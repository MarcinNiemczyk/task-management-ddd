from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.domain.exceptions.base import EntityNotFoundException, DomainException
from src.domain.exceptions.task_exceptions import TaskDeadlineExceedsProjectDeadlineException


async def entity_not_found_handler(
    request: Request, exc: EntityNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def domain_exception_handler(
    request: Request, exc: DomainException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def task_deadline_exceeds_project_handler(
    request: Request, exc: TaskDeadlineExceedsProjectDeadlineException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
