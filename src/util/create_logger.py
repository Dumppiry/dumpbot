import os
import logging
from logging.handlers import RotatingFileHandler
from .file_utils import get_root_dir


def create_logger(name: str = "dumpbot", level=logging.INFO):
    if os.path.exists(f"{get_root_dir()}/logs") is False:
        os.mkdir(f"{get_root_dir()}/logs")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s]: %(message)s")
    print_handler = logging.StreamHandler()
    print_handler.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        filename=f"{get_root_dir()}/logs/{name}.log",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(print_handler)
    logger.addHandler(file_handler)
    return logger


def get_logger(name: str = "dumpbot"):
    return logging.getLogger(name)
