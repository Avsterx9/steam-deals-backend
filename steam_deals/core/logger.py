import logging
import os
import sys
from pathlib import Path
from typing import Final
from typing import Optional

from pydantic import BaseModel
from pydantic import validator

from steam_deals.config import settings
from steam_deals.core.utils import create_log_file

LOGGER_NAME: Final[str] = 'steam_deals'

LOCATION: Final[str] = (
    '- \x1b[1;34;47m%(name)s:%(relativepath)s:%(funcName)s():\x1b[32;47m%(lineno)d\x1b[0m '
    if settings.LOG_LEVEL.upper() == 'DEBUG'
    else ''
)
LOG_FORMAT: Final[str] = f'%(levelprefix)s | %(asctime)s {LOCATION}| %(message)s'
DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'

LOG_FILENAME: Final[Path] = create_log_file('main')


class PackagePathFilter(logging.Filter):
    """Custom filter which adds %(relativepath)s available to logging formatting."""

    def __init__(self, param=None):
        super().__init__()
        self.param = param  # compress static code formatters warnings

    def filter(self, record: logging.LogRecord) -> bool:
        pathname = record.pathname
        record.relativepath = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                break
        return True


class LogConfig(BaseModel):
    """Logging configuration to be set for the server."""

    # pylint: disable=no-self-argument, no-self-use

    log_level: Optional[str] = None

    # Logging config
    version = 1
    disable_existing_loggers = False

    filters = {
        'myfilter': {
            '()': PackagePathFilter,
            'param': 'noshow',
        }
    }

    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': DATE_FORMAT,
        },
    }

    handlers = {
        'console': {
            'filters': ['myfilter'],
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'file': {
            'filters': ['myfilter'],
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'mode': 'w',
            'encoding': 'utf-8',
            'maxBytes': 5000000,
            'backupCount': 4,
        },
    }

    loggers: Optional[dict] = None
    root: Optional[dict] = None

    @validator('log_level', pre=True, always=True)
    def set_log_level(cls, value):
        return value or 'DEBUG'

    @validator('loggers', pre=True, always=True)
    def set_loggers(cls, value, values):
        return value or {
            LOGGER_NAME: {'handlers': ['console'], 'level': values['log_level']},
        }

    @validator('root', pre=True, always=True)
    def set_root(cls, value, values):
        return value or {'handlers': ['file'], 'level': values['log_level']}
