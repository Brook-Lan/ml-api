# -*- coding: utf-8 -*-
"""
@create Time:2020-01-16

@author:LHQ
"""
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from typing import List

from ml import ModelManager


router = APIRouter()


@router.get("/ml-model/list")
def list_models():
    """列出当前运行的模型
    """
    return ModelManager.list_models()


