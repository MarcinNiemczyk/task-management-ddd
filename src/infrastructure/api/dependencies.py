from typing import Annotated

from fastapi import Depends

from src.domain.ports.unit_of_work import IUnitOfWork
from src.domain.services.deadline_service import DeadlineValidationService
from src.infrastructure.database.repositories.project_repository import \
    ProjectRepository
from src.infrastructure.database.repositories.task_repository import \
    TaskRepository
from src.infrastructure.database.unit_of_work import UnitOfWork


def get_unit_of_work() -> IUnitOfWork:
    return UnitOfWork(
        task_repository_factory=lambda session: TaskRepository(session),
        project_repository_factory=lambda session: ProjectRepository(session),
    )


UoWDependency = Annotated[IUnitOfWork, Depends(get_unit_of_work)]
DeadlineValidationServiceImpl = DeadlineValidationService()
