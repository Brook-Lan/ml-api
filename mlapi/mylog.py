# -*- coding: utf-8 -*-
"""
@create Time:2020-07-02

@author:LHQ
"""
import os
import logging
import logging.config


DIR = os.path.dirname(__file__)
log_conf = os.path.join(DIR, "logging.conf")
logging.config.fileConfig(log_conf)


def get_logger(name="root"):
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Hello Logger!")


