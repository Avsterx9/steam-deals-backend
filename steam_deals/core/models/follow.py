from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from steam_deals.core.db import Base


class Follow(Base):
    __tablename__ = 'follows'

    username = Column(ForeignKey('users.username'), primary_key=True)
    steam_appid = Column(ForeignKey('apps.steam_appid'), primary_key=True)
    price_target = Column(Numeric, nullable=False)
    notification = Column(Boolean, nullable=False)
    app = relationship('App', back_populates='users')
    user = relationship('User', back_populates='apps')
