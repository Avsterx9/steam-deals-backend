import logging
import sys
from typing import Union

from steam_deals.config import ROOT_DIRECTORY

FORMATTER = logging.Formatter('%(levelname)s: (%(filename)s:%(lineno)s) | %(message)s')


def logger_setup(level: Union[int, str] = logging.INFO):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(FORMATTER)
    stream_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(ROOT_DIRECTORY.stem)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
