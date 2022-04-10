from passlib.hash import bcrypt

from repositories.users import UsersRepository
from schemas.users import BaseUserSchema, LoginUserSchema
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

    async def create(self, user: LoginUserSchema):
        return await self.repo.create(username=user.username, password_hash=self.hash_password(password=user.password))

    async def authenticate(self, user: LoginUserSchema):
        found_user = await self.repo.get_where(username=user.username)
        if found_user is not None:
            if not self.verify_password(user.password, found_user.password_hash):
                found_user = None

        return user
