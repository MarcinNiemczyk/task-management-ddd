from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.domain.exceptions.task_exceptions import (
    TaskDeadlineExceedsProjectDeadlineException,
)
from src.domain.exceptions.base import DomainException, EntityNotFoundException
from src.infrastructure.database.config import init_db
from src.infrastructure.database.mappers import start_mappers
from .exception_handlers import (
    domain_exception_handler,
    entity_not_found_handler,
    task_deadline_exceeds_project_handler,
)

from .routers import tasks, projects


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

    app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(
        TaskDeadlineExceedsProjectDeadlineException,
        task_deadline_exceeds_project_handler,
    )

    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(projects.router, prefix="/api/v1")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
