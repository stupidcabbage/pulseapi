import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class UserSchema(BaseModel):
    login: str = Field(
            title="Логин пользователя",
            max_length=30,
            pattern=r"[a-zA-Z0-9-]+",
            examples=["yellowMonkey"],
    )
    email: str = Field(
            title="E-mail пользователя",
            max_length=50,
            min_length=1,
            examples=["yellowstone1980@you.ru"],
            pattern=r"^\S+@\S+\.\S+$",
    )
    country_code: str = Field(
            alias="countryCode",
            title="Двухбуквенный код, уникально идентифицирующий страну",
            max_length=2,
            pattern=r"[a-zA-Z]{2}",
            examples=["RU"]
    )
    is_public: bool = Field(
            alias="isPublic",
            title="Является ли данный профиль публичным.",
            description="Публичные профили доступны другим пользователям:\
                    если профиль публичный, любой пользователь платформы\
                    сможет получить информацию о пользователе.",
            examples=[True, False]
    )
    phone: str | None = Field(
            title="Номер телефона пользователя в формате +123456789",
            pattern=r"\+[\d]+",
            max_length=20,
            examples=["+74951239922"],
            default=None
    )
    image: str | None = Field(
        title="Ссылка на фото для аватара пользователя",
        max_length=200,
        min_length=1,
        examples=["https://http.cat/images/100.jpg"],
        default=None
    )

    class Config:
        from_attributes = True


class UserEditSchema(BaseModel):
    country_code: str | None = Field(
            alias="countryCode",
            title="Двухбуквенный код, уникально идентифицирующий страну",
            max_length=2,
            pattern=r"[a-zA-Z]{2}",
            examples=["RU"],
            default=None
    )
    is_public: bool | None = Field(
            alias="isPublic",
            title="Является ли данный профиль публичным.",
            description="Публичные профили доступны другим пользователям:\
                    если профиль публичный, любой пользователь платформы\
                    сможет получить информацию о пользователе.",
            examples=[True, False],
            default=None
    )
    phone: str | None = Field(
            title="Номер телефона пользователя в формате +123456789",
            pattern=r"\+[\d]+",
            max_length=20,
            examples=["+74951239922"],
            default=None
    )
    image: str | None = Field(
        title="Ссылка на фото для аватара пользователя",
        max_length=200,
        min_length=1,
        examples=["https://http.cat/images/100.jpg"],
        default=None
    )

class UserRegisterSchema(UserSchema):
    password: str = Field(
        min_length=6,
        max_length=100,
        examples=["$aba4821FWfew01#.fewA$"]
    )

    @field_validator("password")
    def password_validator(cls, password: str) -> str:
        if not re.fullmatch(r'^.*(?=.{6,})(?=.*[a-zA-Z])(?=.*\d).*$',
                        password):
            raise ValueError("Ненадежный пароль.")
        return password

        
class FullUserSchema(UserSchema):
    password: str = Field(
        examples=["$aba4821FWfew01#.fewA$"],
        exclude=True
    )
    last_password_change: datetime = Field(exclude=True)


class UserUpdatePasswordSchema(BaseModel):
    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(
        min_length=6,
        max_length=100,
        examples=["$aba4821FWfew01#.fewA$"],
        alias="newPassword"
    )

    @field_validator("new_password")
    def password_validator(cls, password: str) -> str:
        if not re.fullmatch(r'^.*(?=.{6,})(?=.*[a-zA-Z])(?=.*\d).*$',
                        password):
            raise ValueError("Ненадежный пароль.")
        return password


class ProfileSchemaOut(BaseModel):
    profile: UserSchema
