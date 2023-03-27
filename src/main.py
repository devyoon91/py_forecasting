import uvicorn
from fastapi_versioning import VersionedFastAPI
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from common.consts import CONTEXT_PATH
from routes import forecasting_api

# init
app = FastAPI(
    title="Forecasting API",
    description="",
    version="0.0.1",
    redoc_url=None,
)

# include routes
app.include_router(forecasting_api.router, tags=["Forecasting"])

# versioning
# /docs, /v1/docs, /v2/docs
app = VersionedFastAPI(app, version_format='{major}', prefix_format=f"/{CONTEXT_PATH}")

# set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def on_app_start() -> None:
    """
    앱이 시작될 때 구성
    """
    logger.info(f"{app.title}-{app.version} app startup")
    logger.info(f"Swagger docs path -> /{CONTEXT_PATH}/docs")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

