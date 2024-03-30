from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator


class PostTagSchema(BaseModel):
    tag: str = Field(max_length=20)


class PostInSchema(BaseModel):
    content: str = Field(
            max_length=1000,
            description="Текст публикации"
    )
    tags: list[str] = Field(
            description="Список тегов публикации",
    )

    @field_validator("tags")
    def tag_validator(tags: list[str]) -> list[PostTagSchema]:
        for i in tags:
            if len(i) > 20:
                raise ValueError("Value to big!")
        return [PostTagSchema(tag=i) for i in tags]

    @field_serializer("tags", when_used="json")
    def tag_serializer(tags: list[PostTagSchema]) -> list[str]:
        return [i.tag for i in tags]


class PostSchema(PostInSchema):
    id: str = Field(
            description="Уникальный идентификатор публикации,\
                    присвоенный сервером.",
            examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    author: str = Field(description="Автор публикации")
    created_at: datetime = Field(
            description="Серверная дата и время в момент, когда пользователь\
                    отправил данную публикацию. Передается в формате RFC3339.",
            examples=["2006-01-02T15:04:05Z07:00"],
            alias="createdAt"
    )
    likes_count: int = Field(
            description="Число лайков, набранное публикацией.",
            alias="likesCount",
            default=0
    )
    dislikes_count: int = Field(
            description="Число дизлайков, набранное публикацией.",
            alias="dislikesCount",
            default=0
    )
