from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserIn(UserBase):
    password: str


class UserInDb(UserBase):
    hashed_password: str
    timestamp: datetime
    disabled: bool = False
    admin: bool = False
    verified: bool = False


class UserDetailed(UserBase):
    timestamp: datetime
    disabled: bool = False
    admin: bool = False
    verified: bool = False

    class Config:
        orm_mode = True


class UserPublic(BaseModel):
    username: str
    first_name: str
    timestamp: datetime
    disabled: bool = False
    verified: bool = False

    class Config:
        orm_mode = True
