# -*- coding: utf-8 -*-
"""
@create Time:2020-01-09

@author:LHQ
"""
import re
import json

from jieba import Tokenizer

from ml.core.abc import TextProcessorABC
from ml.util import singleton


url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


@singleton
class RawTextProcessor(TextProcessorABC):
    def process(self, text):
        """ 不做任何处理
        """
        return text


@singleton
class TextProcessor(TextProcessorABC):
    def __init__(self, user_dic=None, stopwords_path=None):
        self.tokenizer = Tokenizer()
        if user_dic is not None:
            self.tokenizer.load_userdict(user_dic)   # 加载字典
        self.stop_words = self._load_stopwords(stopwords_path)   # 加载停用词

    def _load_stopwords(self, path):
        stop_words = set() 
        with open(path) as f:
            words = [w.strip() for w in f.readlines()]
            stop_words.update(words)
        return stop_words

    def process(self, text):
        text = url_pattern.sub("", text)
        words = self.tokenizer.cut(text.lower())
        words = [w for w in words if w not in self.stop_words]
        return " ".join(words)


DefaultTextProcessor = TextProcessor