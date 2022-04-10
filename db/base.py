import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_async_engine(os.getenv("DATABASE_URL_ASYNC"))
create_async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
