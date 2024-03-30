import time
from typing import Literal

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.auth.handler import decodeJWT
from src.api.exceptions import BaseRouterException
from src.schemas.users import FullUserSchema
from src.services.users import UsersService
from src.utils.unitofwork import UnitOfWork


class JWTBearer(HTTPBearer):
    def __init__(self, uow: UnitOfWork , auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.uow = uow
        
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise BaseRouterException(status_code=401,
                                          reason="Incorrect authorization schema.")
            verify_jwt_status = await self.verify_jwt(self.uow, credentials.credentials)
            if not verify_jwt_status:
                raise BaseRouterException(status_code=401,
                                          reason="Invalid or expired token.")
            return verify_jwt_status
        else:
            raise BaseRouterException(status_code=401,
                                      reason="Invalid token authorization.")

    async def verify_jwt(self, uow: UnitOfWork,
                         jwtoken: str) -> Literal[False] | FullUserSchema:
        try:
            payload = await decodeJWT(jwtoken)
        except:
            return False
        if payload:
            user = await UsersService().get_user(
                    uow, {"login": payload.get("login")})
            if self._is_token_verified(payload, user):
                return user
        return False

    def _is_token_verified(self, payload: dict, user: FullUserSchema) -> bool:
        if not payload.get("expires") or payload.get("expires") < time.time():
            return False
        if not user:
            return False
        last_password_change = user.last_password_change.timestamp()
        if (not payload.get("created_at") or
            not payload.get("created_at") > last_password_change):
            return False

        return True
