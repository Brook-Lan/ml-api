from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from typing import List
from collections import OrderedDict
import traceback

from ml import ModelManager
from projects.word_checking import WordChecker
from projects.rule import Detector
from config import TAG_TO_INFO
from mylog import get_logger

logger = get_logger()

router = APIRouter()

class Text(BaseModel):
    text: str = Field(..., title="短信内容")


class Args(BaseModel):
    tradeTs: str = Field(..., max_length=17)
    tradeId: str = Field(...)
    data: Text = Field(...)


class ResultItem(BaseModel):
    status: int = Field(..., title="状态: 0 - 检测结果正常  1 - 有检测出不规范内容")
    message: str = Field(..., title="说明")
    data: List[str] = Field([], title="报错信息")


@router.post("/sms-check", response_model=ResultItem)
async def hash_tag(args: Args):
    txt = args.data.text
    if len(txt) == 0:
        logger.warn("发送的短信内容为空")
    else:
        # logger.info("接收到参数:" + txt)
        pass

    # 1.敏感词检测
    try:
        word_checker = WordChecker()
        words_found = word_checker.check(txt)
    except Exception as e:
        logger.error("敏感词检测失败：%s" % e)
        words_found = []

    # 2.模型检测内容约定
    try:
        model = ModelManager.get_model("ShortMessageCheckModel")
        tags = model.predict(txt)
    except Exception as e:
        logger.error("模型预测失败: %s" % e)
        tags = []
    
    try:
        detector = Detector()
        infos = detector.detect(txt)
    except Exception as e:
        logger.error("规则引擎检测失败: %s" % e)
        tags = []
    
    # 3. 整理返回结果
    data = []
    if len(words_found) > 0:
        info = "内容包含敏感词：" + "、".join(words_found)
        data.append(info)
    for tag in tags:
        info = TAG_TO_INFO.get(tag)
        if info is not None:
            data.append(info)
    for info in infos:
        if info not in data:
            data.append(info)
    
    if len(data) > 0:
        status = 1
        message = "检测到内容异常"
    else:
        status = 0
        message = "未检测到异常"
    return ResultItem(status=status, message=message, data=data)
