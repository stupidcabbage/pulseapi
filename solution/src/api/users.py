from typing import Annotated

from fastapi import APIRouter, Path

from src.api.dependencies import JWTAuth, UOWDep
from src.api.exceptions import BaseRouterException
from src.schemas.statuses import OKStatus
from src.schemas.users import (UserEditSchema, UserSchema,
                               UserUpdatePasswordSchema)
from src.services.users import UsersService

router = APIRouter()


@router.get(path="/me/profile",
            response_model_exclude_none=True,
            tags=["me"])
async def get_my_profile(user: JWTAuth) -> UserSchema:
    return user


@router.patch(path="/me/profile",
              response_model_exclude_none=True,
              tags=["me"])
async def edit_profile(fields: UserEditSchema,
                       uow: UOWDep,
                       user: JWTAuth) -> UserSchema:
    data = fields.model_dump(exclude_none=True)
    if not data:
        raise BaseRouterException("Необходимо указать хотя бы одно поле.",
                                   400)
    new_user = await UsersService().edit_user(
        uow, user.login, data)
    return new_user


@router.post(path="/me/updatePassword",
             tags=["me"])
async def update_password(passwords: UserUpdatePasswordSchema,
                          uow: UOWDep, user: JWTAuth) -> OKStatus:
    if not await UsersService().update_password(uow, user, passwords):
        raise BaseRouterException("Указанный пароль не соответствует действительности",
                                  403)
    return OKStatus


@router.get(path="/profiles/{login}",
            tags=["me"],
            response_model_exclude_none=True)
async def get_profile(user: JWTAuth,
                      uow: UOWDep,
                      login: Annotated[
                          str, Path(max_length=30, pattern=r"[a-zA-Z0-9-]+",
                                    example="yellowMonkey")]) -> UserSchema:
    profile = await UsersService().get_foreign_profile(uow, user, login)
    return profile
