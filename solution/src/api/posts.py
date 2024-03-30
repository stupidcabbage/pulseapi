from typing import Annotated

from fastapi import APIRouter, Path

from src.api.dependencies import JWTAuth, PaginationDep, UOWDep
from src.schemas.posts import PostInSchema, PostSchema
from src.services.posts import PostsService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/new", summary="Отправить публикацию")
async def add_new_post(uow: UOWDep, user: JWTAuth,
                       post: PostInSchema) -> PostSchema:
    return await PostsService().add_post(uow, user.login, post)


@router.get("/{postID}")
async def get_post(uow: UOWDep, user: JWTAuth,
                   postID: Annotated[str, Path()]) -> PostSchema:
    return await PostsService().get_post(uow, user.login, {"id": postID})


@router.get("/feed/my")
async def get_my_feed(uow: UOWDep, user: JWTAuth,
                      pagination: PaginationDep) -> list[PostSchema]:
    return await PostsService().get_posts(uow, from_login=user.login,
                                          login=user.login,
                                          limit=pagination.get("limit"),
                                          offset=pagination.get("offset"))


@router.get("/feed/{login}")
async def get_foreign_feed(uow: UOWDep, user: JWTAuth,
                      pagination: PaginationDep,
                      login: Annotated[str, Path()]) -> list[PostSchema]:
    return await PostsService().get_posts(uow, from_login=user.login,
                                          login=login,
                                          limit=pagination.get("limit"),
                                          offset=pagination.get("offset"))


@router.post("/{postID}/like")
async def like_post(uow: UOWDep, user: JWTAuth,
                   postID: Annotated[str, Path()]) -> PostSchema:
    return await PostsService().update_vote(uow, user.login, postID, 1)


@router.post("/{postID}/dislike")
async def dislike_post(uow: UOWDep, user: JWTAuth,
                       postID: Annotated[str, Path()]) -> PostSchema:
    return await PostsService().update_vote(uow, user.login, postID, 0)
