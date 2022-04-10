from fastapi import APIRouter, Depends

from api.api_v1.deps import get_current_user
from schemas.users import LoginUserSchema, BaseUserSchema
from services.users import UsersService

router = APIRouter()


@router.post("/")
async def create_user(user: LoginUserSchema):
    async with UsersService() as service:
        await service.create(user)
    return {"message": "ok"}


@router.get("/me/", response_model=BaseUserSchema)
async def get_current_user(user: BaseUserSchema = Depends(get_current_user)):
    return user
