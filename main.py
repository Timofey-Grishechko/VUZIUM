from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.core import (
    get_logger,
    register_exception_handlers,
    settings,
    setup_logging,
)
from internal.core.middleware import RequestContextMiddleware

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...", extra={"ctx_env": settings.env})

    yield

    logger.info("Application shutting down...")



app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,  # <-- ключевое изменение
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)

register_exception_handlers(app)

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.env}


# 8. Routers