from db.urls import Url
from repositories.base import BaseRepository


class UrlsRepository(BaseRepository[Url]):
    async def create(self, username: str, url: str, url_hash: str, ):
        self.session.add(Url(user_username=username, url=url, hash=url_hash))
