import re
import os
from os.path import dirname, abspath, join as join_path

from ml.core.meta import ModelMeta


## 本地文件目录
ROOT_DIR = dirname(abspath(__file__))
DATA_DIR = join_path(ROOT_DIR, "data")
WORDS_DIR = join_path(DATA_DIR, "words")
os.makedirs(DATA_DIR, exist_ok=True)

## 敏感词文件路径
SENSITIVE_WORDS_FILE = join_path(WORDS_DIR, "banned_word.txt")

# 提示信息
INFO = {
    "info_1":"结构性存款应提示：“结构性存款不同于一般性存款，具有投资风险，您应当充分认识投资风险，谨慎投资”",
    "info_2":"公募基金应提示：“本产品由xx基金公司发行与管理，浦发银行作为代销机构不承担产品的投资、兑付和风险管理责任”、“基金由风险，投资需谨慎”",
    "info_3":"无需添加TDDX退订短信提示",
    "info_4":"理财产品需提示：“理财非存款，产品有风险，投资需谨慎”",
    "info_5":"不能宣传预期收益率，说历史业绩的，需说明具体的数据统计时间，要说结构性存款产品过往业绩不代表其未来表现，不等于结构性存款产品实际收益",
    "info_6":"理财产品有收益率应提示：“理财产品过往业绩不代表其未来表现、不等于理财产品实际收益”",    
}

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


## 模型预测的标签 --> 提示信息 的映射关系
TAG_TO_INFO = {
    "tag_other": None,    # "正常"
    "tag_1": INFO["info_1"],
    "tag_2": INFO["info_2"],
    "tag_3": INFO["info_3"],
    "tag_4": INFO["info_4"],
    "tag_5": INFO["info_5"],
    "tag_6": INFO["info_6"],
}

# 规则配置
RULES = {
    "conditions" : [
        ("基金", "F1"),
        ("本产品由", "F2"),
        ("基金公司发行与管理，浦发银行作为代销机构不承担产品的投资、兑付和风险管理责任", "F3"),
        ("基金有风险，投资需谨慎", "F4"),
    ],

    "rules" : [
        (["F1", "-F2", "-F3", "-F4"], INFO["info_2"]),
    ]
}
