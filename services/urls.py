import binascii
import os
from hashlib import md5
from typing import List

from fastapi import HTTPException

from repositories.urls import UrlsRepository
from schemas.urls import BaseUrlSchema, UrlSchema
from schemas.users import BaseUserSchema
from services.base import BaseService


class UrlsService(BaseService[UrlSchema, UrlsRepository]):
    ALLOWED_SYMBOLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # [0-9A-Za-z]

    async def __aenter__(self):
        return self

    @classmethod
    def hash_url(cls, url: str) -> str:
        salt = binascii.hexlify(os.urandom(5)).decode()
        url += salt
        hex_int = int(md5(url.encode()).hexdigest(), 16)
        digits = []
        if hex_int == 0:
            digits.append(0)
        else:
            while hex_int and len(digits) < 8:
                digits.append(hex_int % 62)
                hex_int //= 62

        return "".join([cls.ALLOWED_SYMBOLS[i] for i in digits])

    async def create(self, url: BaseUrlSchema, user: BaseUserSchema):
        url_hash = self.hash_url(url.url)
        while (n := await self.get_where(hash=url_hash)) is not None:
            url_hash = self.hash_url(url.url)
        await self.repo.create(username=user.username, url=url.url, url_hash=url_hash)
        return UrlSchema(url=url.url, hash=url_hash, user=user)

    async def get_and_visit(self, url_hash: str):
        url = await self.repo.get_where(hash=url_hash)
        if not url:
            raise HTTPException(status_code=404, detail="Not found")
        url.increase_visits()
        return UrlSchema.from_orm(url)

    async def get_all_where_order_by(self, order_by: str = 'id', asc=True, **filters, ) -> List[UrlSchema]:
        return self.convert_all(await self.repo.get_all_where_order_by(order_by, asc, **filters))

    async def delete_by_id(self, user: BaseUserSchema, id: int):
        if (await self.get_where(id=id)).user.username == user.username:
            await self.repo.delete_by_id(id)
        else:
            raise HTTPException(status_code=403, detail="Can't delete other user's url")
