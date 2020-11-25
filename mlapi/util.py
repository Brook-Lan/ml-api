# -*- coding: utf-8 -*-
"""
@create Time:2020-01-16

@author:LHQ
"""

def singleton(cls):
    """单例装饰器
    """
    _instances = {}
    def _singleton():
        if cls not in _instances:
            _instances[cls] = cls()
        return _instances[cls]
    return _singleton
