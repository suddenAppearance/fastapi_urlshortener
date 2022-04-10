from hashlib import md5

from repositories.urls import UrlsRepository
from schemas.urls import BaseUrlSchema
from schemas.users import BaseUserSchema
from services.base import BaseService


class UrlsService(BaseService[BaseUrlSchema, UrlsRepository]):

    ALLOWED_SYMBOLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # [0-9A-Za-z]

    @classmethod
    def hash_url(cls, url: str) -> str:
        hex_int = int(md5(url.encode()).hexdigest(), 16)
        digits = []  # wont even reverse
        if hex_int == 0:
            digits.append(0)
        else:
            while hex_int and len(digits) < 6:
                digits.append(hex_int % 62)
                hex_int //= 62


    async def create(self, url: BaseUrlSchema, user: BaseUserSchema):
        await self.repo.create()
