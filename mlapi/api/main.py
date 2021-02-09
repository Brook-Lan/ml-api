# -*- coding: utf-8 -*-
"""
@create Time:2020-01-11

@author:LHQ
"""
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from ml import ModelManager
from projects.word_checking import WordChecker
from projects.rule import Detector
from config import MODEL_METAS, SENSITIVE_WORDS_FILE, RULES

from .routers import mlmodel, check
from mylog import get_logger


logger = get_logger()

app = FastAPI()


@app.on_event("startup")
async def start_event():
    """应用启动时的一些初始化"""
    # 加载机器学习模型
    logger.info("加载机器学习模型")
    ModelManager.load_models(MODEL_METAS)

    # 初始化基于规则的检测器
    logger.info("初始化规则引擎")
    try:
        detector = Detector()
        detector.load(RULES)
    except Exception as e:
        logger.error("规则引擎初始化失败：%s" %e)

    # 实例化WordsChecker类(单例), 加载敏感词
    logger.info("初始化禁用词检测器")
    try:
        word_checker = WordChecker()
        word_checker.add_keywords_from_file(SENSITIVE_WORDS_FILE)
    except Exception as e:
        logger.error("禁用词检测器初始化失败：%s" %e)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(exc)
    return await request_validation_exception_handler(request, exc)


app.include_router(
        check.router,
        prefix="/api/v1",
        tags=["SMS Check"],
        responses={404: {"description": "Not found"}}
        )
app.include_router(mlmodel.router,
        tags=["Model"]
        )
