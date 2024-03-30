import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.db.models.users import User
from src.schemas.posts import PostSchema, PostTagSchema


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column()
    author_login: Mapped[str] = mapped_column(ForeignKey("users.login"))
    author: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[List["Tag"]] = relationship(back_populates="post",
                                             lazy="subquery")
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    reacts: Mapped[List["Like"]] = relationship()
    
    def to_read_model(self) -> PostSchema:
        return PostSchema(
            id=str(self.id),
            content=self.content,
            author=self.author_login,
            createdAt=(self.created_at).strftime("%Y-%m-%dT%H:%M:%S.%f"),
            tags=[]
        )



class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column()
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="tags")

    def to_read_model(self) -> PostTagSchema:
        return PostTagSchema(tag=self.tag)
