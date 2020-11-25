# -*- coding: utf-8 -*-
"""
@create Time:2019-09-25

@author:LHQ
"""
import os
from importlib import import_module


def load_object(path):
    """Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not full path " % path)

    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named %s" % (module, name))

    return obj


def load_ml_model_from_meta(meta):
    """实例化机器学习模型
    """
    clf_modelfile = meta.CLF_MODEL_FILE
    lb_modelfile = meta.LB_MODEL_FILE
    ModelClass = load_object(meta.MODEL_CLASS)
    TextProcessor = load_object(meta.PROCESSOR_CLASS)
    processor = TextProcessor(**meta.PROCESSOR_INIT_KWARGS)   # 实例化数据预处理类实例
    model_obj = ModelClass(clf_modelfile, lb_modelfile, processor)
    return model_obj
