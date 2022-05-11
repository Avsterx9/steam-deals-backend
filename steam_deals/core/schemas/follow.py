from typing import Optional

from pydantic import BaseModel


class FollowBase(BaseModel):
    username: str
    price_target: Optional[float] = None

    class Config:
        orm_mode = True


class FollowIn(FollowBase):
    steam_appid: int
    notification: Optional[bool] = False
