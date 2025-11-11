from uuid import UUID

from fastapi import APIRouter, status

from src.application.use_cases.projects.create_project import (
    CreateProjectCommand,
    CreateProjectUseCase,
)
from src.application.use_cases.projects.get_all_projects import GetAllProjectsUseCase
from src.application.use_cases.projects.get_project import GetProjectUseCase
from src.application.use_cases.projects.update_project import (
    UpdateProjectCommand,
    UpdateProjectUseCase,
)
from src.infrastructure.api.dependencies import UoWDependency
from src.infrastructure.api.schemas.project_schemas import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Creates a new project with the provided details.",
)
def create_project(
    project_in: ProjectCreateRequest,
    uow: UoWDependency,
) -> ProjectResponse:
    command = CreateProjectCommand(
        title=project_in.title,
        deadline=project_in.deadline,
    )

    project = CreateProjectUseCase(uow).execute(command)

    return ProjectResponse.from_entity(project)


@router.get(
    "/",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all projects",
    description="Retrieves a list of all projects.",
)
def get_all_projects(
    uow: UoWDependency,
) -> list[ProjectResponse]:
    projects = GetAllProjectsUseCase(uow).execute()
    return [ProjectResponse.from_entity(project) for project in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a project by ID",
    description="Retrieves a project by its unique ID.",
)
def get_project(
    project_id: UUID,
    uow: UoWDependency,
) -> ProjectResponse:
    project = GetProjectUseCase(uow).execute(project_id)
    return ProjectResponse.from_entity(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a project",
    description="Updates the details of an existing project.",
)
def update_project(
    project_id: UUID,
    project_in: ProjectUpdateRequest,
    uow: UoWDependency,
) -> ProjectResponse:
    command = UpdateProjectCommand(
        title=project_in.title,
        deadline=project_in.deadline,
    )

    project = UpdateProjectUseCase(uow).execute(project_id, command)

    return ProjectResponse.from_entity(project)
