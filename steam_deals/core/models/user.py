from sqlalchemy import Boolean, Column, DateTime, String

from steam_deals.core.db.base_class import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String, nullable=False, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=False), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)
    verified = Column(Boolean, nullable=False, default=False)
