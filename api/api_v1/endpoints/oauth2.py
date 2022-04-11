from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from core import settings
from schemas.users import BaseUserSchema, LoginUserSchema
from services.users import UsersService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth2/token")


async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Optional[BaseUserSchema]:
    async with UsersService() as service:
        user: Optional[BaseUserSchema] = await service.authenticate(LoginUserSchema(username=form_data.username, password=form_data.password))

    return user


@router.post("/token/")
async def obtain_token(user: Optional[BaseUserSchema] = Depends(authenticate_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = jwt.encode(user.dict(), settings.SECRET_KEY, algorithm='HS256')

    return {"access_token": token, "token_type": "bearer"}
