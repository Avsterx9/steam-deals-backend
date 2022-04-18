import datetime
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class AppBase(BaseModel):
    steam_appid: int
    app_type: str
    name: str
    header_image: str
    developers: List[str] = []
    publishers: List[str] = []
    screenshots: List[str] = []
    short_description: Optional[str] = None
    is_free: Optional[bool] = None
    price: Optional[Dict[str, float]] = None
    release_date: Optional[datetime.datetime] = None
