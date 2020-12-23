#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2020-12-18

@author:LHQ
"""
from projects.rule import Detector
from config import RULES


if __name__ == "__main__":
    detector = Detector()
    detector.load(RULES)

    msg = detector.detect("本产品")
    print(msg)
