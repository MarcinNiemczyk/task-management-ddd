from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.database.config import init_db
from src.infrastructure.database.mappers import start_mappers

from .routers import tasks


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Management API",
        description="DDD-based Task Management System with Hexagonal Architecture",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_db()
    start_mappers()

    app.include_router(tasks.router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
