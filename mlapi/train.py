# -*- coding: utf-8 -*-
"""
@create Time:2020-11-25

@author:LHQ
"""
import os
import pickle
import re
import json

import click
import numpy as np
import pandas as pd
from jieba import Tokenizer
import fasttext
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import hamming_loss, f1_score, classification_report

from ml.default.process import DefaultTextProcessor
from config import processor_init_kwargs


base_dir = os.path.dirname(__name__)
data_dir = os.path.join(base_dir, "data")
model_dir = os.path.join(data_dir, "sms")


class TrainConfig:
    # common parameters
    threshold = 0.5   #  概率阈值
    # 训练/测试数据位置
    train_path = os.path.join(data_dir, "train_data/shortcontent_train.csv")

    ## sklearn 模型保存位置
    sklearn_mlb_file = os.path.join(data_dir, "hashtag/shortcontent_mlb.pkl")   # 标签转换器模型文件
    sklearn_clf_file = os.path.join(data_dir, "hashtag/shortcontent_clf.pkl")  # 分类器模型文件

    ## fasttext 模型保存位置
    fasttext_clf_file = os.path.join(data_dir, "hashtag/shortcontent_clf_fasttext.bin")


def preprocessing(df):
    """ 数据预处理
    """
    df = df.copy()
    processor = DefaultTextProcessor(**processor_init_kwargs)
    df["token"] = df["content"].map(processor.process)
    data = []
    y = []
    for token, gp in df.groupby("token"):
        tags = gp["tag"].unique().tolist()
        if len(tags) > 1 and "other" in tags:
            tags.remove("other")
        data.append(token)
        y.append(tags)
    return data, y


def train_sklearn(x_train, y_train, x_test, y_test, config):
    """sklearn 模型训练
    """
    clf_file = config.sklearn_clf_file
    mlb_file = config.sklearn_mlb_file
    threshold = config.threshold
    ## 多标签二值化
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_train)
    # 参数搜索
    print("参数搜索...")
    grid_params = {"estimator__C":[100,130,150,180, 200, 250,300]}
    clf = OneVsRestClassifier(LogisticRegression(solver="lbfgs", max_iter=600))
    pipe_search = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("featselect", SelectPercentile(score_func=chi2, percentile=15)),
        ("grid_search", GridSearchCV(clf, grid_params, "f1_micro", cv=10)),
    ])
    pipe_search.fit(x_train, y)
    best_C = pipe_search["grid_search"].best_params_["estimator__C"]
    print(best_C)
    # 模型训练
    print("模型训练...")
    model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2))),
                      ("featselect", SelectPercentile(score_func=chi2, percentile=15)),
                      ("clf", OneVsRestClassifier(LogisticRegression(solver="lbfgs",C=best_C, max_iter=600))),
                     ])
    model.fit(x_train, y)
    # 模型验证
    print("验证...")
    y_pred = model.predict(x_test)
    y_true = mlb.transform(y_test)
    validate(y_true, y_pred, mlb.classes_.tolist())
    # 模型保存
    print("模型保存...")
    save_sklearn_model(mlb, mlb_file)
    save_sklearn_model(model, clf_file)
    print("done!")


def save_sklearn_model(model, model_path):
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)


def train_fasttext(x_train, y_train, x_test, y_test, config):
    """fasttext 模型训练
    """
    model_file = config.fasttext_clf_file
    threshold = config.threshold   # 概率阈值
    ## 多标签二值化
    mlb = MultiLabelBinarizer()
    mlb.fit(y_train)
    ## 整理成fasttext输入文件形式
    train_path = "tmp_train.data"
    with open(train_path, "w") as f:
        for txt, tags in zip(x_train, y_train):
            label = " ".join(map(lambda x: "__label__%s"%x, tags))
            line = "%s %s\n" % (label, txt)
            f.write(line)
    # 模型训练
    model = fasttext.train_supervised(train_path, 
                                      epoch=500,
                                      dim=50,
                                      lr=0.2,
                                      wordNgrams=2,
                                      neg=5,
                                      ws=5,
                                      lrUpdateRate=95,
                                      loss="ova"
                                      )
    ## 模型预测
    y_pred_ = model.predict(x_test, k=-1)
    y_pred = []
    for _, (lb, proba) in enumerate(zip(*y_pred_)):
        inds, *_ = np.where(proba > threshold)
        inds = inds.tolist()
        labels = [lb[ind].split("__")[-1] for ind in inds]
        if len(labels) > 1 and "other" in labels:
            labels.remove("other")
        if len(labels) == 0:
            labels.append("other")
        y_pred.append(labels)
    # 标签编码
    y_pred = mlb.transform(y_pred)
    y_true = mlb.transform(y_test)
    validate(y_true, y_pred, mlb.classes_.tolist())
    # 模型保存
    model.save_model(model_file)


def validate(y_true, y_pred, target_names=None):
    ## 评估指标: F1 和 Hamming Loss
    print("======性能指标======")
    print("Hamming Loss:", hamming_loss(y_true, y_pred))
    print("F1_score:", f1_score(y_true, y_pred, average="micro"))
    print("======详细报告======")
    # print(classification_report(y_true, y_pred,target_names=mlb.classes_.tolist()))
    print(classification_report(y_true, y_pred, target_names=target_names))


@click.command()
@click.option("--method", type=click.Choice(["sklearn", "fasttext"]), default="fasttext", help="模型类型")
def main(method):
    trains = {
        "sklearn": train_sklearn,
        "fasttext": train_fasttext,
    }
    train = trains[method]
    ## 读取文件
    df = pd.read_csv(TrainConfig.train_path).dropna()
    ## 预处理
    x, y = preprocessing(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    ## 模型训练
    train(x_train, y_train, x_test, y_test, TrainConfig)


if __name__ == "__main__":
    main()

