import jwt
from fastapi import Depends, HTTPException, status

from api.api_v1.endpoints.oauth2 import oauth2_scheme
from core import settings
from schemas.users import BaseUserSchema
from services.users import UsersService


async def get_current_user(token: str = Depends(oauth2_scheme)) -> BaseUserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', ])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    async with UsersService() as service:
        user = await service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
