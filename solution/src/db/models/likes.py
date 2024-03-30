import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.db import Base
from src.schemas.likes import ReactSchema


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
            UniqueConstraint("user_login", "post_id", "vote"),
    )

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    user_login: Mapped[str] = mapped_column(ForeignKey("users.login"))
    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id"))
    vote: Mapped[int] = mapped_column()
    
    def to_read_model(self) -> ReactSchema:
        return ReactSchema(
                author=self.user_login,
                post_id=str(self.post_id),
                vote=self.vote
        )
