import re

from src.repositories.excpetions import ProfileAccessDenied
from src.schemas.likes import ReactSchema
from src.schemas.posts import PostInSchema, PostSchema
from src.services.users import UsersService
from src.utils.unitofwork import IUnitOfWork


class PostsService:
    ID_REGEX = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    async def add_post(self, uow: IUnitOfWork, from_login: str,
                       post: PostInSchema) -> PostSchema:
        async with uow:
            new_post = await uow.posts.add_one(data={"author_login": from_login,
                                                 "content": post.content})
            all_tags = []
            for i in post.tags:
                tag = await uow.tags.add_one(data={"post_id": new_post.id,
                                                   "tag": i.tag})
                all_tags.append(tag)
            new_post.tags = all_tags
            await uow.commit()
            return new_post

    async def get_post(self, uow: IUnitOfWork, from_login: str,
                       data: dict[str, list | str]) -> PostSchema:
        async with uow:
            if data.get("id"):
                is_valid = re.match(self.ID_REGEX, data.get("id"))
                if not is_valid:
                    raise ProfileAccessDenied(reason="Публикации не существует.",
                                              status_code=404)

            post = await uow.posts.get_where(data=data)
            post.likes_count, post.dislikes_count = await self.get_reacts(uow, post.id)
            if not post:
                raise ProfileAccessDenied(reason="Публикации не существует.")
            if not await UsersService().is_user_has_access(uow, from_login,
                                                                post.author):
                raise ProfileAccessDenied(reason="Нет доступа к публикации.",
                                          status_code=404)
            return post

    async def get_posts(self, uow: IUnitOfWork, from_login: str, login: str,
                        limit: int, offset: int) -> list[PostSchema]:
        async with uow:
            if not await UsersService().is_user_has_access(uow, from_login,
                                                           login):
                raise ProfileAccessDenied(reason="Нет доступа к публикациям.",
                                          status_code=404)

            posts = await uow.posts.pagination_get(data={"author_login": login},
                                                   limit=limit, offset=offset,
                                                   order_by="created_at")
            for i in posts:
                i.likes_count, i.dislikes_count = await self.get_reacts(uow, i.id)
            return posts

    async def update_vote(self, uow: IUnitOfWork, user_login: str, post_id: str,
                          vote: int) -> PostSchema:
        async with uow:
            post = await self.get_post(uow, user_login, data={"id": post_id})

            if not post:
                raise ProfileAccessDenied(reason="Пост не найден",
                                          status_code=404)

            if not await UsersService().is_user_has_access(uow, user_login,
                                                           post.author):
                raise ProfileAccessDenied(reason="Нет доступа к публикации.",
                                          status_code=404)

            react = await self.get_react(uow, user_login, post.id)
            if not react:
                react = await uow.likes.add_one(data={"post_id": post_id,
                                                "user_login": user_login,
                                                "vote": vote})
                if vote:
                    post.likes_count += 1
                else:
                    post.dislikes_count += 1

            elif react.vote != vote:
                await uow.likes.edit_one(post_id=post_id,
                                         user_login=user_login,
                                         data={"vote": vote})
                if vote:
                    post.dislikes_count -= 1
                    post.likes_count += 1
                else:
                    post.likes_count -= 1
                    post.dislikes_count += 1
                    
            await uow.commit()
            return post

    async def get_react(self, uow: IUnitOfWork, user_login, post_id: str) -> ReactSchema:
        like = await uow.likes.get_where(
                data={"post_id": post_id,
                      "user_login": user_login})
        return like

    async def get_reacts(self, uow: IUnitOfWork,
                         post_id: str) -> tuple[int, int]:
        likes_count = await uow.likes.get_count(data={"post_id": post_id,
                                                      "vote": 1})
        dislikes_count = await uow.likes.get_count(data={"post_id": post_id,
                                                         "vote": 0})
        return (likes_count, dislikes_count)
