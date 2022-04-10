from typing import Optional

from fastapi import HTTPException
from passlib.hash import bcrypt

from repositories.users import UsersRepository
from schemas.users import BaseUserSchema, LoginUserSchema, DBUserSchema
from services.base import BaseService


class UsersService(BaseService[BaseUserSchema, UsersRepository]):
    async def __aenter__(self):  # this is pure copying, but PyCharm doesn't show proper type hinting
        return self

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str):
        return bcrypt.verify(password, password_hash)

    async def get_by_username(self, username: str):
        return await self.get_where(username=username)

    async def __get_full_user_by_username(self, username: str) -> Optional[DBUserSchema]:
        return DBUserSchema.from_orm(await self.repo.get_where(username=username))

    async def create(self, user: LoginUserSchema):
        if (n := await self.get_by_username(username=user.username)) is not None:
            raise HTTPException(status_code=409, detail=f"'{user.username}' is already taken")

        return await self.repo.create(username=user.username, password_hash=self.hash_password(password=user.password))

    async def authenticate(self, user: LoginUserSchema):
        found_user = await self.__get_full_user_by_username(username=user.username)
        if found_user is not None:
            if not self.verify_password(user.password, found_user.password_hash):
                found_user = None

        return found_user
