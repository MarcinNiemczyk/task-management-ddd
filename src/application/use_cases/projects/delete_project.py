from uuid import UUID

from src.domain.ports.unit_of_work import IUnitOfWork


class DeleteProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, project_id: UUID) -> None:
        with self.uow.transaction():
            self.uow.project_repository.delete_project_tasks(project_id)
            self.uow.project_repository.delete(project_id)
            
