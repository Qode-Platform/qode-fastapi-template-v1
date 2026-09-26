"""Entrypoint: `uvicorn app.main:app --reload`."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open pools, warm caches
    yield
    # shutdown: close them


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(items.router)
