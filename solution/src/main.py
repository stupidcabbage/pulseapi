from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.api.exceptions import (BaseRouterException, base_exception_handler,
                                db_unique_exception_handler,
                                doesnot_exists_handler,
                                profile_access_denied_exception_handler,
                                validation_exception_handler)
from src.api.routers import all_routers
from src.repositories.excpetions import (DBUniqueException,
                                         DoesNotExistsException,
                                         ProfileAccessDenied)

app = FastAPI(root_path="/api")


for i in all_routers:
    app.include_router(i)
app.add_exception_handler(DoesNotExistsException, doesnot_exists_handler)
app.add_exception_handler(BaseRouterException, base_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DBUniqueException, db_unique_exception_handler)
app.add_exception_handler(ProfileAccessDenied, profile_access_denied_exception_handler)
