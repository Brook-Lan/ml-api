# -*- coding: utf-8 -*-
"""
@create Time:2019-09-25

@author:LHQ
"""


def singleton(cls):
    """单例装饰器
    """
    _instances = {}
    def _singleton(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return _singleton
