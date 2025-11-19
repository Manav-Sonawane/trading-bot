import logging
from logging.handlers import RotatingFileHandler
import sys


def configure_logging():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)

    # avoid duplicate handlers if called twice
    if logger.handlers:
        return logger

    fmt = "%(asctime)s | %(levelname)5s | %(name)s | %(message)s"
    formatter = logging.Formatter(fmt)

    # console logger (INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # file logger (DEBUG)
    fh = RotatingFileHandler("bot.log", maxBytes=5_000_000, backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # silence noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger
