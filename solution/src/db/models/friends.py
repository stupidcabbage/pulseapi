from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.schemas.friends import FriendSchema


class Friend(Base):
    __tablename__ = "friends"
    __table_args__ = (
            UniqueConstraint("added_user_login", "who_added_user_login"),
    )

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    added_user_login: Mapped[str] = mapped_column(ForeignKey("users.login"))
    who_added_user_login: Mapped[str] = mapped_column(ForeignKey("users.login"))
    added_user: Mapped["User"] = relationship("User", foreign_keys=added_user_login)
    who_added_user: Mapped["User"] = relationship("User",
                                                  back_populates="friends",
                                                  foreign_keys=who_added_user_login)
    added_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    
    def to_read_model(self) -> FriendSchema:
        return FriendSchema(
            added=self.who_added_user_login,
            login=self.added_user_login,
            addedAt=(self.added_at).isoformat()
        )
