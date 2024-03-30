from src.db.models.posts import Post, Tag
from src.repositories.repository import SQLAlchemyRepository


class PostsRepositories(SQLAlchemyRepository):
    model = Post


class TagsRepositories(SQLAlchemyRepository):
    model = Tag