from fastapi import APIRouter

from src.api.dependencies import JWTAuth, PaginationDep, UOWDep
from src.schemas.friends import FriendOutInSchema, FriendSchema
from src.schemas.statuses import OKStatus
from src.services.friends import FriendsService

router = APIRouter(prefix="/friends", tags=["friends"])


@router.post("/add")
async def add_friend(uow: UOWDep, user: JWTAuth,
                     data: FriendOutInSchema) -> OKStatus:
    await FriendsService().add_friend(uow,
                                      from_login=user.login,
                                      login=data.login)
    return OKStatus


@router.post("/remove")
async def remove_friend(uow: UOWDep, user: JWTAuth,
                        data: FriendOutInSchema) -> OKStatus:
    await FriendsService().remove_friend(uow,
                                         from_login=user.login,
                                         login=data.login)
    return OKStatus


@router.get("")
async def get_friends(uow: UOWDep, user: JWTAuth,
                      pagination: PaginationDep) -> list[FriendSchema]:
    friends = await FriendsService().get_friends(uow, from_login=user.login,
                                       limit=pagination.get("limit"),
                                       offset=pagination.get("offset"))
    return friends

