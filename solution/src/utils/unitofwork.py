from abc import ABC, abstractmethod
from typing import Type

from src.db.db import async_session_maker
from src.repositories.countries import CountriesRepository
from src.repositories.friends import FriendsRepository
from src.repositories.likes import LikesRepositories
from src.repositories.posts import PostsRepositories, TagsRepositories
from src.repositories.users import UsersRepository


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    tags: Type[TagsRepositories]
    posts: Type[PostsRepositories]
    countries: Type[CountriesRepository]
    friends: Type[FriendsRepository]
    likes: Type[LikesRepositories]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.countries = CountriesRepository(self.session)
        self.tags = TagsRepositories(self.session)
        self.posts = PostsRepositories(self.session)
        self.friends = FriendsRepository(self.session)
        self.likes = LikesRepositories(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
