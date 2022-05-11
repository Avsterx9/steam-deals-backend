from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from steam_deals.core.db import Base


class App(Base):
    __tablename__ = 'apps'

    steam_appid = Column(BigInteger, nullable=False, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    header_image = Column(Text, nullable=False)
    developers = Column(Text, nullable=False)
    publishers = Column(Text, nullable=False)
    price = Column(Numeric, nullable=False)
    users = relationship('Follow', back_populates='app')
