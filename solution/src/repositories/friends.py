from src.db.models.users import Friend
from src.repositories.repository import SQLAlchemyRepository


class FriendsRepository(SQLAlchemyRepository):
    model = Friend
