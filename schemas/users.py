from pydantic import BaseModel, Field


class BaseUserSchema(BaseModel):
    username: str = Field(..., min_length=8, regex="[a-zA-Z0-9_]", max_length=32)


class LoginUserSchema(BaseUserSchema):
    password: str
