from typing import Annotated

from fastapi import Depends

from src.api.auth.bearer import JWTBearer
from src.api.pagination import get_pagination_params
from src.schemas.users import FullUserSchema
from src.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
JWTAuth = Annotated[FullUserSchema, Depends(JWTBearer(UnitOfWork()))]
PaginationDep = Annotated[dict, Depends(get_pagination_params)]
