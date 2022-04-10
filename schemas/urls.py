from pydantic import BaseModel

from schemas.users import BaseUserSchema


class BaseUrlSchema(BaseModel):
    url: str


class UrlSchema(BaseModel):
    id: int
    hash: str
    url: str
    user: BaseUserSchema

    class Config:
        orm_mode = True
