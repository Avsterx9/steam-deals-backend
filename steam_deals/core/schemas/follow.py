from typing import Optional

from pydantic import BaseModel

from steam_deals.core.schemas.app import AppBaseInDb


class FollowBase(BaseModel):
    username: str
    price_target: Optional[float] = None


class FollowPublic(FollowBase):
    class Config:
        orm_mode = True


class FollowIn(FollowBase):
    steam_appid: int
    notification: Optional[bool] = False


class FollowDetailed(FollowPublic, FollowIn):
    app: AppBaseInDb
