import logging
import os
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent

LOGS = Path.joinpath(BASEDIR, "logs")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    
    if not os.path.exists(os.path.join(BASEDIR, "logs")):
        os.makedirs(os.path.join(BASEDIR, "logs"))

    handler = logging.FileHandler(os.path.join(LOGS, log_file), mode="w")        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
