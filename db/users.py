from sqlalchemy import Column, String

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, primary_key=True, index=True)
    password_hash = Column(String)