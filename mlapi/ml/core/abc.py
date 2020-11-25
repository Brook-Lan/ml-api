# -*- coding: utf-8 -*-
"""
@create Time:2019-09-24

@author:LHQ

机器学习模型接口类

"""
from abc import ABC, abstractmethod


class MLModelABC(ABC):
    """模型抽象类"""
    def __init__(self, clf_modelfile, lb_modelfile=None, process_text=None):
        pass

    @abstractmethod
    def predict(self, data):
        pass


class TextProcessorABC(ABC):
    """文本预处理器抽象类"""
    @abstractmethod
    def process(self, text):
        pass



