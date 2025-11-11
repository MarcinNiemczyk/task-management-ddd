from uuid import UUID

from src.domain.entities.project import Project
from src.domain.ports.unit_of_work import IUnitOfWork


class GetProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, project_id: UUID) -> Project:
        with self.uow.transaction():
            project = self.uow.project_repository.get(project_id)

        return project
