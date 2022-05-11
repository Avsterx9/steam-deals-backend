from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from steam_deals.core.db.base_class import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(Text, nullable=False, primary_key=True, index=True)
    email = Column(Text, nullable=False, unique=True, index=True)
    hashed_password = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=False), nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)
    verified = Column(Boolean, nullable=False, default=False)
    apps = relationship('Follow', back_populates='user', cascade='all, delete-orphan')
