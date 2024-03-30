import datetime
from typing import Literal

import bcrypt

from src.repositories.excpetions import (CountryDoesNotExists,
                                         ProfileAccessDenied)
from src.schemas.tokens import SignInSchema
from src.schemas.users import (FullUserSchema, UserRegisterSchema,
                               UserUpdatePasswordSchema)
from src.services import friends
from src.services.countries import CountriesService
from src.utils.unitofwork import IUnitOfWork


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UserRegisterSchema):
        if not await self._is_country_exists(uow, user.country_code):
            raise CountryDoesNotExists

        user.password = self._hash_password(user.password)
        user_dict = user.model_dump(by_alias=False)
        async with uow:
            user = await uow.users.add_one(data=user_dict)
            await uow.commit()
            return user

    async def get_user(self, uow: IUnitOfWork, data: dict[str, list | str]):
        async with uow:
            return await uow.users.get_where(data=data)

    async def edit_user(self, uow: IUnitOfWork,
                        login: str, data: dict[str, str]):
        if (data.get("country_code") and
            not await self._is_country_exists(uow, data.get("country_code"))):
            raise CountryDoesNotExists(status_code=400)
        
        async with uow:
            user = await uow.users.edit_one(data=data, login=login)
            await uow.commit()
            return user

    async def _is_country_exists(self, uow: IUnitOfWork,
                                 alpha2: str) -> bool:
        country = await CountriesService().get_country_by(
                uow, {"alpha2": alpha2})
        return bool(country)

    async def get_foreign_profile(self, uow: IUnitOfWork,
                                  user: FullUserSchema, login: str) -> FullUserSchema:
        if not await self.is_user_has_access(uow, user.login, login):
            raise ProfileAccessDenied(reason="Пользователя не существует")

        profile = await self.get_user(uow, {"login": login})

        return profile

    async def is_user_has_access(self, uow: IUnitOfWork, from_login: str, login: str) -> bool:
        if from_login  == login:
            return True

        profile = await self.get_user(uow, {"login": login})
        if not profile:
            return False
        
        if not profile.is_public:
            if not await friends.FriendsService().get_friend(uow, login, from_login):
                return False
        return True
    
    async def update_password(self, uow: IUnitOfWork,
                              user: FullUserSchema, 
                              passwords: UserUpdatePasswordSchema) -> bool:
        if await self.verify_password(user, passwords.old_password):
            new_password = self._hash_password(passwords.new_password)
            await self.edit_user(uow, login=user.login, data={"password": new_password,
                                                        "last_password_change": datetime.datetime.now()})
            return True
        return False
    
    async def verify_password(self, user, password: str) -> bool:
        check_password = user.password.encode()
        is_valid = bcrypt.checkpw(password.encode(), check_password)
        if is_valid:
            return True
        return False

    async def authenticate_user(self, uow: IUnitOfWork,
                                data: SignInSchema) -> Literal[False] | str:
        user = await self.get_user(uow, data={"login": data.login})
        if not user:
            return False
        if not await self.verify_password(user, data.password):
            return False
        return user.login

    def _hash_password(self, password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return str(hash_.decode())
    
