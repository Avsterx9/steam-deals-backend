import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel


class PriceOverview(BaseModel):
    final: Optional[float] = None
    initial: Optional[float] = None
    discount: Optional[float] = None


class OwnersOverview(BaseModel):
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None


class AppBase(BaseModel):
    steam_appid: int
    name: str
    index: Optional[int] = None
    ccu_yesterday: int
    header_image: str
    developers: List[str] = []
    publishers: List[str] = []
    positive: Optional[int] = None
    negative: Optional[int] = None
    positive_percent: Optional[float] = None
    owners: OwnersOverview
    price: PriceOverview


class AppDetailed(AppBase):
    app_type: str
    screenshots: List[str] = []
    short_description: Optional[str] = None
    release_date: Optional[datetime.datetime] = None
