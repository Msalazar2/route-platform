from fastapi import FastAPI
from .core.config import settings
from .routers import health, notes
from .core.cors import add_cors

app = FastAPI(title=settings.PROJECT_NAME)

add_cors(app)  # enable CORS for dev

app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])
app.include_router(notes.router,  prefix=settings.API_PREFIX, tags=["notes"])
