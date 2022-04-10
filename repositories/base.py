from typing import TypeVar, Generic, get_args, List, Optional, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import create_async_session, Base

DBModel = TypeVar('DBModel')


class DBException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors


class BaseRepository(Generic[DBModel]):

    def __init__(self):
        self.session: AsyncSession = create_async_session()
        self.model: Type[DBModel] = get_args(self.__orig_bases__[0])[0]  # lol this actually works:P

    async def close(self):
        if self.session is not None:
            try:
                await self.session.commit()
            except Exception as e:
                await self.session.rollback()
                raise DBException(*e.args)
            finally:
                try:
                    await self.session.close()
                except Exception as e:
                    raise DBException(*e.args)

    async def get_all(self, limit: int, offset: int) -> List[DBModel]:
        result = await self.session.execute(select(self.model).limit(limit).offset(offset))
        return result.scalars().all()

    async def get_all_where(self, **filters) -> List[DBModel]:
        result = await self.session.execute(select(self.model).filter(
            *[getattr(self.model, key) == value for key, value in filters.items()]
        ))
        return result.scalars().all()

    async def get_where(self, **filters) -> Optional[DBModel]:
        result = await self.session.execute(select(self.model).filter(
            *[getattr(self.model, key) == value for key, value in filters.items()]
        ))
        return result.scalars().one_or_none()
