from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserIn(UserBase):
    password: str


class User(UserBase):
    timestamp: datetime
    disabled: bool

    class Config:
        orm_mode = True


class UserInDb(UserBase):
    hashed_password: str
    timestamp: datetime
    disabled: bool
