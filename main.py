from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time, logging
from .db import engine, Base
from .routes import auth_routes, user_routes, file_routes, health_routes

app = FastAPI(title="Labmentixx Backend")

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(file_routes.router)
app.include_router(health_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.access")

class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} completed in {duration:.2f}s")
        return response

app.add_middleware(RequestTimingMiddleware)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
