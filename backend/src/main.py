"""FastAPI application entrypoint.

Registers routers and middleware. Must not trigger any database
connection or other side effects at import time.
"""

from fastapi import FastAPI

from src.adapters.inbound.api.health_router import router as health_router
from src.config.settings import settings

app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(health_router)
