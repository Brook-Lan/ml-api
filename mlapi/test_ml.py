# -*- coding: utf-8 -*-
"""
@create Time:2020-01-16

@author:LHQ
"""
from ml import ModelManager
from config import MODEL_METAS


ModelManager.load_models(MODEL_METAS)


if __name__ == "__main__":
    model = ModelManager.get_model("ShortMessageCheckModel")

    s = "优于别人，并不高贵，真正的高贵应该是优于过去的自己。"
    s = "昨晚涨点，今天就割了，这是玩过家家😅😅"
    s = "btc继续收敛式横盘，貌似有利空方，下步再下一波的概率在增加柚子火腿"
    pred = model.predict(s)
    print(pred, s)
