from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.repositories.excpetions import (DBUniqueException,
                                         DoesNotExistsException,
                                         ProfileAccessDenied)


class BaseRouterException(Exception):
    def __init__(self, reason: str, status_code: int):
        self.reason = reason
        self.status_code = status_code


async def base_exception_handler(request: Request, exc: BaseRouterException):
    return JSONResponse(
            status_code=exc.status_code,
            content={"reason": exc.reason})


async def doesnot_exists_handler(request: Request, exc: DoesNotExistsException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"reason": exc.reason})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"reason":
                 _generate_validation_exception_reason(exc)}
    )


async def db_unique_exception_handler(request: Request, exc: DBUniqueException):
    return JSONResponse(
        status_code=409,
        content={"reason": "Значение не уникально."}
    )


async def profile_access_denied_exception_handler(request: Request, exc: ProfileAccessDenied):
    return JSONResponse(
        status_code=exc.status_code,
        content={"reason": exc.reason}
    )


def _generate_validation_exception_reason(exc: RequestValidationError):
    error = exc.errors()[0]
    return f"Field: {error.get("loc")[-1]}. Error: {error.get('msg')}"
