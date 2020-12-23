#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2020-11-24

@author:LHQ
"""
from collections import namedtuple

from utils.flashtext import KeywordProcessor
from utils.decorators import singleton


Rule = namedtuple("Rule", ["expression", "message"])


@singleton
class Detector:
    def __init__(self):
        self.processor = KeywordProcessor()
        self.processor.set_non_word_boundaries([])
        self.conditions = set()
        self.rules = []

    def load(self, conf):
        """
        """
        conditions = conf["conditions"]
        rules = conf["rules"]
        for cond, cid in conditions:
            self.add_condition(cond, cid)
        for rule, target in rules:
            self.add_rule(rule, target)

    def add_condition(self, condition, condition_id):
        """添加判断条件（关键词)
        Args
        ----
        condition : str, 用于匹配文本的一些关键词，可以是字符串

        condition_id : str, 不能以"-"开头。 与condition对应的，用于后续的rule配置

        Examples
        --------
        >>> detector.add_condition("回复TDDX退订资讯短信", "c_1")
        >>> detector.add_condition("理财非存款，产品有风险，投资需谨慎", "c_2")
        >>> detector.add_condition("本产品由", "c_3-1")
        >>> detector.add_condition("基金公司发行与管理，浦发银行作为代销机构不承担产品的投资、兑付和风险管理责任", "c_3-2")
        """
        if isinstance(condition, list):
            for cond  in condition:
                self.add_condition(cond, condition_id)
        elif isinstance(condition, str):
            self.processor.add_keyword(condition, condition_id)
            self.conditions.add(condition_id)
        else:
            raise ValueError("condition must be a string or string list, but received %s" % condition)

    def add_rule(self, rule_expr, rule_message):
        """添加规则
        Args
        ----
        rule_expr : str list, 基于condition组合的判定规则，列表中的各个condition
                之间是'与'的关系，condition前面加'-'表示取反
        rule_message : str, 该规则的描述，当文本命中该规则时会返回该描述

        Examples
        --------
        >>> detector.add_rule(["-c_3"], "短信内容需包括风险提示")
        """
        rule = Rule(expression=rule_expr, message=rule_message)
        self.rules.append(rule)

    def detect(self, text):
        keywords = self.processor.extract_keywords(text)
        result = []
        for rule in self.rules:
            flag = True
            for cond in rule.expression:
                if cond.startswith("-"):
                    cond = cond.lstrip("-")
                    flag_  = not cond in keywords
                else:
                    flag_ = cond in keywords
                flag = flag and flag_
            if flag:
                result.append(rule.message)
        return result
            

if __name__ == "__main__":
#    keyword_processor = KeywordProcessor()
#    keyword_processor.add_keyword_from_file("data/words.txt")
#    keywords_found = keyword_processor.extract_keywords("世界第一")

    detector = Detector()
    detector.add_condition("回复TDDX退订资讯短信", "fund_1")
    detector.add_condition("基金有风险，投资需谨慎", "fund_2")
    detector.add_condition("理财非存款，产品有风险，投资需谨慎", "dep_1")
    detector.add_condition("本产品由", "c_3-1")
    detector.add_condition("基金公司发行与管理，浦发银行作为代销机构不承担产品的投资、兑付和风险管理责任", "c_3-2")

    detector.add_rule(["-fund_1", "-fund_2"], "公募基金。。。")
    detector.add_rule(["-c_3-1, -c_3-2"], "缺少免责申明")

    print(detector.detect("本产品由"))
    
