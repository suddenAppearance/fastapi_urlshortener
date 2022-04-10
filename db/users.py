from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    username = Column(String(32), unique=True, primary_key=True, index=True)
    password_hash = Column(String)

    urls = relationship("Url", back_populates="user")