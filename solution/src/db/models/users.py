from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.db.models.friends import Friend
from src.schemas.users import FullUserSchema, UserSchema


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
            UniqueConstraint("login", "email", "phone", name="user_uc"),
    )

    login: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    country_code: Mapped[str] = mapped_column(ForeignKey("countries.alpha2",
                                                         use_alter=True))
    is_public: Mapped[bool] = mapped_column(default=True)
    phone: Mapped[str | None] = mapped_column(unique=True,
                                              nullable=True,
                                              default=None)
    image: Mapped[str | None] = mapped_column(nullable=True,
                                              default=None)
    last_password_change: Mapped[datetime] = mapped_column(insert_default=func.now())
    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    friends: Mapped[List["Friend"]] = relationship(
            back_populates="who_added_user",
            foreign_keys=Friend.who_added_user_login)
    reacts: Mapped[List["Like"]] = relationship()
                                                   

    def to_read_model(self) -> UserSchema:
        return FullUserSchema(
                login=self.login,
                email=self.email,
                countryCode=self.country_code,
                isPublic=self.is_public,
                phone=self.phone,
                image=self.image,
                password=self.password,
                last_password_change=self.last_password_change
        )
