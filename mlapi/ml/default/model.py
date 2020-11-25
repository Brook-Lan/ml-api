# -*- coding: utf-8 -*-
"""
@create Time:2020-01-08

@author:LHQ
"""
import warnings
import pickle
from operator import itemgetter

import fasttext

from ml.core.abc import MLModelABC, TextProcessorABC
from .process import DefaultTextProcessor, RawTextProcessor


def dump_model(model, model_path):
    """训练模型序列化
    """
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


def load_model(model_path):
    """模型反序列化
    """
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        return model


class SklearnModel(MLModelABC):
    def __init__(self, clf_modelfile, lb_modelfile=None, processor=RawTextProcessor()):
        self.processor= processor
        self.clf = load_model(clf_modelfile)
        self.lb = load_model(lb_modelfile) if lb_modelfile is not None else None

    def predict(self, text, threshold=None):
        assert isinstance(text, str), "'text' must be a string"
        # 文本预处理(分词、去标点等)
        X = self.processor.process(text)
        # 模型分类
        pred = self.clf.predict([X])
        # 预测结果转换成字符
        if self.lb is not None:
            pred = self.lb.inverse_transform(pred)
        return pred[0]


class SklearnOrderlyModel(SklearnModel):
    """ predecit方法返回按概率从大到小排序的标签
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, text, threshold=0.5):
        # 文本预处理(分词、去标点等)
        X = self.processor.process(text)
        # 模型分类
        probas = self.clf.predict_proba([X])[0]

        if self.lb is not None:
            classes_ = self.lb.classes_
        else:
            classes_ = self.clf.classes_
        pred = filter(lambda x: x[0] > threshold, zip(probas, classes_))
        pred = sorted(pred, key=itemgetter(0), reverse=True)
        return [tag for p, tag in pred]


class FasttextModel(MLModelABC):
    """fasttext模型
    """
    def __init__(self, clf_modelfile, lb_modelfile=None, processor=RawTextProcessor()):
        self.processor= processor
        self.model = fasttext.load_model(clf_modelfile)

    def predict(self, text, threshold=0.5):
        X = self.processor.process(text)
        classes_, probas = self.model.predict(X, k=-1)
        pred = filter(lambda x: x[0] > threshold, zip(probas, classes_))
        pred = sorted(pred, key=itemgetter(0), reverse=True)
        return [tag.replace("__label__", "") for p, tag in pred]

