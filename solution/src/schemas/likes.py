from pydantic import BaseModel


class ReactSchema(BaseModel):
    author: str
    post_id: str
    vote: int
