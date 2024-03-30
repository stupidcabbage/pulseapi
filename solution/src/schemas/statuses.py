from pydantic import BaseModel, Field


class OKStatus(BaseModel):
    status: str = Field(default="ok")
