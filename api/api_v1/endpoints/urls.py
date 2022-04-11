from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from api.api_v1.deps import get_current_user
from schemas.urls import BaseUrlSchema
from schemas.users import BaseUserSchema
from services.urls import UrlsService

router = APIRouter()


@router.post("/")
async def create_url(url: BaseUrlSchema, user: BaseUserSchema = Depends(get_current_user)):
    async with UrlsService() as service:
        await service.create(url, user)


@router.get("/")
async def get_my_urls(user: BaseUserSchema = Depends(get_current_user)):
    async with UrlsService() as service:
        return await service.get_all_where(user_username=user.username)


@router.get("/{url_hash}/")
async def get_real_url(url_hash: str):
    async with UrlsService() as service:
        url = await service.get_and_visit(url_hash=url_hash)
        return RedirectResponse(url=url.url)
