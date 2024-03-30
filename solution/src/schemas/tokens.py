from pydantic import BaseModel


class TokenSchema(BaseModel):
    token: str


class SignInSchema(BaseModel):
    login: str
    password: str
