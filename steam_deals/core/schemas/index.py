from typing import Final

from pydantic import BaseModel

from steam_deals.config import settings, VERSION

TITLE: Final[str] = settings.PROJECT_TITLE
DESCRIPTION: Final[str] = settings.PROJECT_DESC
MESSAGE: Final[str] = 'For documentation please refer to /docs endpoint'


class Index(BaseModel):
    title: str = TITLE
    description: str = DESCRIPTION
    message: str = MESSAGE
    version: str = VERSION

    def __repr__(self):
        return str(self.__dict__)
