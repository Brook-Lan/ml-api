from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from typing import List
from collections import OrderedDict
import traceback

from ml import ModelManager
from projects.word_checking import WordChecker
from projects.rule import Detector
from config import TAG_TO_INFO


router = APIRouter()

class Args(BaseModel):
    text: str = Field(..., title="短信内容")


class ResultItem(BaseModel):
    status: int = Field(..., title="状态: 0 - 正常  1 - 有检测出信息")
    message: str = Field(..., title="说明")
    data: List[str] = Field(..., title="报错信息")


@router.post("/sms-check", response_model=ResultItem)
async def hash_tag(args: Args):
    txt = args.text
    # 1.敏感词检测
    word_checker = WordChecker()
    words_found = word_checker.check(txt)

    # 2.模型检测内容约定
    # tags = []
    model = ModelManager.get_model("ShortMessageCheckModel")
    tags = model.predict(txt)

    detector = Detector()
    infos = detector.detect(txt)
    
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
    return dict(status=status, message=message, data=data)
