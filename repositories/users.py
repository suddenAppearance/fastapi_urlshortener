from db.users import User
from repositories.base import BaseRepository


class UsersRepository(BaseRepository[User]):
    def create(self, username: str, password_hash: str):
        self.session.add(User(username=username, password_hash=password_hash))
