from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    hash = Column(String(8), unique=True, index=True)
    url = Column(String)
    visits = Column(Integer, default=0)

    user_username = Column(String, ForeignKey("users.username"))

    user = relationship("User", back_populates="urls", lazy="selectin")

    # this will increase value via SQL, not Python.
    # 1 query and no race condition
    def increase_visits(self):
        self.visits = self.visits + 1
