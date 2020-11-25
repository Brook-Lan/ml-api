import re
import os
from os.path import dirname, abspath, join as join_path

from ml.core.meta import ModelMeta


## 本地文件目录
ROOT_DIR = dirname(abspath(__file__))
DATA_DIR = join_path(ROOT_DIR, "data")
WORDS_DIR = join_path(DATA_DIR, "words")
os.makedirs(DATA_DIR, exist_ok=True)


##==================== 模型的meta描述,该meta描述将被用于实例化一个模型================##
# MODEL_NAME : 模型的名称，自定义，但不要重复 
# MODEL_CLASS : 模型的类， 如："ml.models.hashtag.HashTagModel"
# PROCESSOR_CLASS : 文本预处理类
# PROCESSOR_INIT_KWARGS : processor类的实例化参数, dict形式
# CLF_MODEL_FILE : 模型序列化后的文件位置
# LB_MODEL_FILE : 标签label的转换器（transformer）序列化后的文件位置
default_processor_cls = "ml.default.process.DefaultTextProcessor"
processor_init_kwargs = {"stopwords_path": join_path(WORDS_DIR, "stopwords.txt"),
                         "user_dic": join_path(WORDS_DIR, "mydic.dic")}
MODEL_METAS = [
    # ModelMeta(MODEL_NAME="HashTagArticleModel", 
    #           MODEL_CLASS="ml.default.model.SklearnOrderlyModel",
    #           PROCESSOR_CLASS=default_processor_cls,
    #           PROCESSOR_INIT_KWARGS=processor_init_kwargs,
    #           CLF_MODEL_FILE=join_path(DATA_DIR, "hashtag/article_clf.pkl"),
    #           LB_MODEL_FILE=join_path(DATA_DIR, "hashtag/article_mlb.pkl"),
    #           ), 
    ModelMeta(MODEL_NAME="ShortMessageCheckModel",
              MODEL_CLASS="ml.default.model.FasttextModel",
              PROCESSOR_CLASS=default_processor_cls,
              PROCESSOR_INIT_KWARGS=processor_init_kwargs,
              CLF_MODEL_FILE=join_path(DATA_DIR, "models/sms_clf_fasttext.bin"),
              LB_MODEL_FILE=None, 
              ),
]


## 敏感词文件路径
SENSITIVE_WORDS_FILE = join_path(WORDS_DIR, "sensitive_words.txt")

## 模型预测的标签 --> 提示信息 的映射关系
TAG_TO_INFO = {
    "0":"正常",
    "1":"未附加‘退订提示’",
    "2":"无2",
    "3":"无3",
    "4":"无4",
    "5":"无5",
    "6":"无6",
    "BTC": "btc123",
    "EOS": "eos321",
    "ETH": "eth00000",
    "HT": "ht66666"
}