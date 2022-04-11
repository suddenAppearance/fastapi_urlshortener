from sqlalchemy import select, delete

from db.urls import Url
from repositories.base import BaseRepository


class UrlsRepository(BaseRepository[Url]):
    async def create(self, username: str, url: str, url_hash: str, ):
        self.session.add(Url(user_username=username, url=url, hash=url_hash))

    async def get_all_where_order_by(self, order_by: str, asc=True, **filters):
        statement = select(self.model).filter(
            *[getattr(self.model, key) == value for key, value in filters.items()]
        )
        if asc:
            statement = statement.order_by(getattr(self.model, order_by))
        else:
            statement = statement.order_by(getattr(self.model, order_by).desc())
        result = await self.session.execute(statement)
        return result.scalars().all()


    async def delete_by_id(self, id: int):
        await self.session.execute(delete(self.model).filter(self.model.id == id))
