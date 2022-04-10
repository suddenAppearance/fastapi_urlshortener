import uvicorn
from fastapi import FastAPI

from api.api_v1 import api

app = FastAPI()

app.include_router(api.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
