# -*- coding: utf-8 -*-
"""
@create Time:2020-01-19

@author:LHQ

@info: ModelMeta用于在配置文件中描述一个模型的基本信息，
       可根据ModelMeta信息来实例化一个模型
"""
from collections import namedtuple


# MODEL_NAME : 模型的名称 
# MODEL_CLASS : 模型的类， 如："ml.models.hashtag.HashTagModel"
# PROCESSOR_CLASS : 文本预处理类
# PROCESSOR_INIT_KWARGS : processor类的实例化参数, dict形式
# CLF_MODEL_FILE : 模型序列化后的文件位置
# LB_MODEL_FILE : 标签label的转换器（transformer）序列化后的文件位置
ModelMeta = namedtuple("ModelMeta",
                       ["MODEL_NAME",
                        "CLF_MODEL_FILE", 
                        "LB_MODEL_FILE",
                        "PROCESSOR_INIT_KWARGS",
                        "PROCESSOR_CLASS",
                        "MODEL_CLASS", 
                       ])

default_processor_init_kwargs = dict()
default_processor_cls = "ml.default.process.DefaultTextProcessor"
default_model_cls = "ml.default.model.SklearnModel"
ModelMeta.__new__.__defaults__ = (default_processor_init_kwargs, default_processor_cls, default_model_cls)