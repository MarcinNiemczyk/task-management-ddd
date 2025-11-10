from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.tasks.create_task import (CreateTaskCommand,
                                                         CreateTaskUseCase)
from src.infrastructure.api.dependencies import UoWDependency
from src.infrastructure.api.schemas.task_schemas import (TaskCreateRequest,
                                                         TaskResponse)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with the provided details.",
)
def create_task(
    task_in: TaskCreateRequest,
    uow: UoWDependency,
) -> TaskResponse:
    command = CreateTaskCommand(
        title=task_in.title,
        description=task_in.description,
        deadline=task_in.deadline,
        project_id=task_in.project_id,
    )

    use_case = CreateTaskUseCase(uow)
    task = use_case.execute(command)

    return TaskResponse.from_entity(task)
