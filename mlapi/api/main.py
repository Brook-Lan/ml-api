# -*- coding: utf-8 -*-
"""
@create Time:2020-01-11

@author:LHQ
"""
from fastapi import Depends, FastAPI, Header, HTTPException

from ml import ModelManager
from projects.word_checking import WordChecker
from config import MODEL_METAS, SENSITIVE_WORDS_FILE

from .routers import mlmodel, check


app = FastAPI()


@app.on_event("startup")
async def start_event():
    """应用启动时的一些初始化"""
    # 加载机器学习模型
    ModelManager.load_models(MODEL_METAS)

    # 实例化WordsChecker类(单例), 加载敏感词
    word_checker = WordChecker()
    word_checker.add_keywords_from_file(SENSITIVE_WORDS_FILE)


app.include_router(
        check.router,
        prefix="/api/v1",
        tags=["SMS Check"],
        responses={404: {"description": "Not found"}}
        )
app.include_router(mlmodel.router,
        tags=["Model"]
        )
