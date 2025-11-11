from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.tasks.create_task import (CreateTaskCommand,
                                                         CreateTaskUseCase)
from src.application.use_cases.tasks.delete_task import DeleteTaskUseCase
from src.application.use_cases.tasks.get_all_tasks import GetAllTasksUseCase
from src.application.use_cases.tasks.get_task import GetTaskUseCase
from src.application.use_cases.tasks.update_task import (UpdateTaskCommand,
                                                         UpdateTaskUseCase)
from src.infrastructure.api.dependencies import UoWDependency, DeadlineValidationServiceImpl
from src.infrastructure.api.schemas.task_schemas import (TaskCreateRequest,
                                                         TaskResponse,
                                                         TaskUpdateRequest)

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

    task = CreateTaskUseCase(uow).execute(command)

    return TaskResponse.from_entity(task)


@router.get(
    "/",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieves a list of all tasks, with optional filtering.",
)
def get_all_tasks(
    uow: UoWDependency,
    completed: bool | None = None,
    overdue: bool | None = None,
    project_id: UUID | None = None,
) -> list[TaskResponse]:
    tasks = GetAllTasksUseCase(uow).execute(
        completed=completed,
        overdue=overdue,
        project_id=project_id,
    )
    return [TaskResponse.from_entity(task) for task in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a task by ID",
    description="Retrieves a task by its unique ID.",
)
def get_task(
    task_id: UUID,
    uow: UoWDependency,
) -> TaskResponse:
    task = GetTaskUseCase(uow).execute(task_id)
    return TaskResponse.from_entity(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Updates the details of an existing task.",
)
def update_task(
    task_id: UUID,
    task_in: TaskUpdateRequest,
    uow: UoWDependency,
) -> TaskResponse:
    command = UpdateTaskCommand(
        title=task_in.title,
        description=task_in.description,
        deadline=task_in.deadline,
    )

    task = UpdateTaskUseCase(uow, DeadlineValidationServiceImpl).execute(task_id, command)

    return TaskResponse.from_entity(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Deletes a task by its unique ID.",
)
def delete_task(
    task_id: UUID,
    uow: UoWDependency,
) -> None:
    DeleteTaskUseCase(uow).execute(task_id)

