from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router

from contextlib import asynccontextmanager
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: You could add a DB health check here if desired
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Lender Backend API"}
