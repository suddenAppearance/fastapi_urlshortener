from typing import Optional

from pydantic import BaseModel, AnyUrl

from schemas.users import BaseUserSchema


class BaseUrlSchema(BaseModel):
    url: str


class UrlSchema(BaseModel):
    id: Optional[int]
    hash: str
    url: AnyUrl
    visits: int = 0
    user: BaseUserSchema

    class Config:
        orm_mode = True
