from steam_deals.config import VERSION
from steam_deals.config import settings
from steam_deals.core.schemas.app import *
from steam_deals.core.schemas.follow import *
from steam_deals.core.schemas.other import *
from steam_deals.core.schemas.token import *
from steam_deals.core.schemas.user import *


class Index(BaseModel):
    title: str = settings.PROJECT_TITLE
    description: str = settings.PROJECT_DESC
    message: str = 'For documentation please refer to /docs endpoint'
    version: str = VERSION

    def __repr__(self):
        return str(self.__dict__)
