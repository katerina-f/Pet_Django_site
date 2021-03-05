import sys
import logging


FORMAT = '[%(asctime)s]%(name)s::%(funcName)s[%(lineno)d]: %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)


def get_custom_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.level = logging.DEBUG
    return logger
