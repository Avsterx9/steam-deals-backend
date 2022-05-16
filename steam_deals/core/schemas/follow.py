from typing import Optional

from pydantic import BaseModel


class FollowBase(BaseModel):
    username: str
    steam_appid: int
    price_target: Optional[float] = None
    notification: Optional[bool] = False
