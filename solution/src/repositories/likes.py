from src.db.models.likes import Like
from src.repositories.repository import SQLAlchemyRepository


class LikesRepositories(SQLAlchemyRepository):
    model = Like