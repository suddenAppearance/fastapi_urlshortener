import os.path

from fastapi import APIRouter, Request
from starlette.responses import FileResponse

from api.api_v1.endpoints import oauth2, users, urls

router = APIRouter()

router.include_router(oauth2.router, prefix="/oauth2", tags=["oauth2"])
router.include_router(users.router, prefix="/users", tags=['users'])
router.include_router(urls.router, prefix="", tags=['urls'])


