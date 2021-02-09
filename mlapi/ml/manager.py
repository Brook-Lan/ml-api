# -*- coding: utf-8 -*-
"""
@create Time:2020-01-19

@author:LHQ
"""
import warnings

from .core.abc import MLModelABC
from .core.exceptions import ModelNotFoundException
from .core.loader import load_ml_model_from_meta
from mylog import get_logger


logger = get_logger()


class ModelManager:
    """管理所有机器学习模型
    """
    _models = dict()

    @classmethod
    def load_models(cls, metas):
        """加载模型
        Args
        ----
        metas : List[namedtuple], namedtuple的定义参看 ml.ml_config.MODEL_META 
        model_name : str, 要载入的模型模型名称，为None则表示载入所有模型
        update: bool, 载入模型前是不是要重下下载更新模型，默认不要

        Returns
        -------
        loaded_models: list， 成功载入的模型
        """
        print("load ml model...")
        loaded_models = []
        for meta in metas:
            meta_model_name = meta.MODEL_NAME
            try:
                model_obj = load_ml_model_from_meta(meta)
            except Exception as e:
                # warnings.warn("加载模型(%s)失败:%s"%(meta_model_name, e))
                logger.error("加载模型(%s)失败:%s"%(meta_model_name, e))
                continue
            if isinstance(model_obj, MLModelABC):
                cls._models[meta_model_name] = {"obj": model_obj, "meta": meta._asdict()}
                loaded_models.append(meta_model_name)
        return loaded_models

    @classmethod
    def get_model(cls, model_name):
        model = cls._models[model_name]["obj"]
        return model

    @classmethod
    def list_models(cls):
        return {name: {"obj": str(item["obj"]), "meta":item["meta"]} for name, item in cls._models.items()}

