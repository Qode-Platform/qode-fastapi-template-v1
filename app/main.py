"""Entrypoint: `uvicorn app.main:app --reload`."""

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.base_path import base_path
from app.config import get_settings
from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open pools, warm caches
    yield
    # shutdown: close them


settings = get_settings()
BASE_PATH = base_path()

# The docs/schema URLs are absolute, so they need the prefix baked in too.
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url=f"{BASE_PATH}/docs",
    redoc_url=f"{BASE_PATH}/redoc",
    openapi_url=f"{BASE_PATH}/openapi.json",
)

# Everything hangs off one prefixed router, so a single line moves the whole
# app under the ingress path (and an empty BASE_PATH leaves it at the root).
root = APIRouter(prefix=BASE_PATH)


@root.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


root.include_router(items.router)
app.include_router(root)
