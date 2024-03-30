from pydantic import BaseModel, Field


class FriendOutInSchema(BaseModel):
    login: str = Field(max_length=30,
                       pattern=r"[a-zA-Z0-9-]+",
                       examples=["yellowMonkey"])


class FriendSchema(BaseModel):
    added: str = Field(description="Login добавившего",
                       exclude=True)
    add: str = Field(description="Login добавленного",
                     alias="login")
    added_at: str = Field(description="Дата добавления в формате RFC3339",
                          alias="addedAt")
