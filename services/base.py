import traceback
from typing import TypeVar, Generic, get_args, List, Optional, Type

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, IntegrityError

from repositories.base import DBException

RepositoryModel = TypeVar('RepositoryModel')
SchemaModel = TypeVar('SchemaModel')


class BaseService(Generic[SchemaModel, RepositoryModel]):
    def __init__(self):
        self.schema: Type[SchemaModel] = get_args(self.__orig_bases__[0])[0]
        self.repo: RepositoryModel = get_args(self.__orig_bases__[0])[1]()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.repo.close()
        except DBException:
            raise HTTPException(status_code=400, detail=f"{str(exc_val)}")

        if exc_type in [DBAPIError, IntegrityError]:
            raise HTTPException(status_code=409, detail=f"{exc_val._message()}")

        if exc_type == HTTPException:
            raise exc_val

        elif exc_val is not None:
            raise HTTPException(status_code=500,
                                detail=f"Internal server error. {exc_type}: {exc_val}\n{traceback.format_tb(exc_tb)}")

    def convert_all(self, instances) -> List[SchemaModel]:
        return self.__convert_all(instances)

    def __convert_all(self, instances) -> List[SchemaModel]:
        return [self.__convert(db_user) for db_user in instances]

    def __convert(self, instance) -> SchemaModel:
        return self.schema.from_orm(instance)

    async def get_all(self, limit, offset) -> List[SchemaModel]:
        db_users = await self.repo.get_all(limit, offset)
        return self.__convert_all(db_users)

    async def get_all_where(self, **filters) -> List[SchemaModel]:
        db_users = await self.repo.get_all_where(**filters)
        return self.__convert_all(db_users)

    async def get_where(self, **filters) -> Optional[SchemaModel]:
        db_user: Optional[SchemaModel] = await self.repo.get_where(**filters)
        return self.__convert(db_user) if db_user is not None else None
