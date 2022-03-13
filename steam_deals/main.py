import argparse
import logging
import sys
from typing import Sequence

import uvicorn

from steam_deals.config import ROOT_DIRECTORY, settings, VERSION
from steam_deals.core.logger import logger_setup

log = logging.getLogger(ROOT_DIRECTORY.stem)


def init_argparse(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=settings.PROJECT_TITLE, formatter_class=argparse.RawTextHelpFormatter)

    add = parser.add_argument
    add('--host', type=str, default=settings.HOST, help=f'Server host address. (default: {settings.HOST})')
    add('-p', '--port', type=int, default=settings.PORT, help=f'Server port number. (default: {settings.PORT})')

    return parser.parse_args(args)


def main():
    args = init_argparse(sys.argv[1:])
    logger_setup(level=settings.LOG_LEVEL.upper())
    log.info(f'VERSION: {VERSION}')

    uvicorn.run(
        app='steam_deals.v1.api:app',
        host=args.host,
        port=args.port,
        debug=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == '__main__':
    main()
