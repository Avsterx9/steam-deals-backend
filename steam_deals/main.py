import argparse
import logging.config
import sys
from typing import Sequence

import uvicorn

from steam_deals.config import VERSION
from steam_deals.config import settings
from steam_deals.core.db.base_class import Base
from steam_deals.core.logger import LogConfig

logging.config.dictConfig(LogConfig(log_level=settings.LOG_LEVEL).dict())
log = logging.getLogger('steam_deals')


def init_argparse(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=settings.PROJECT_TITLE, formatter_class=argparse.RawTextHelpFormatter)

    add = parser.add_argument
    add('--host', type=str, default=settings.HOST, help=f'Server host address. (default: {settings.HOST})')
    add('-p', '--port', type=int, default=settings.PORT, help=f'Server port number. (default: {settings.PORT})')

    return parser.parse_args(args)


def main():
    log.debug('DEBUGGING MODE IS ENABLED')
    log.info(f'VERSION: {VERSION}')
    log.info(f'ENVIRONMENT: {settings.ENV_FOR_DYNACONF}')

    try:
        args = init_argparse(sys.argv[1:])
    except AttributeError:
        log.critical(f'Error in  `{settings.ENV_FOR_DYNACONF}` ENVIRONMENT')
        raise AttributeError(f'ENVIRONMENT `{settings.ENV_FOR_DYNACONF}` doest not exist / has missing args ') from None

    # pylint: disable= import-outside-toplevel
    # Wee need to import after try except block if we want to catch this error
    from steam_deals.core.db.session import engine

    Base.metadata.create_all(bind=engine)

    uvicorn.run(
        app='steam_deals.v1.api:app',
        host=args.host,
        port=args.port,
        debug=settings.LOG_LEVEL.upper() == 'DEBUG',
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == '__main__':
    main()
