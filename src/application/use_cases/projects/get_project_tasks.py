from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


class GetProjectTasksUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, project_id: UUID) -> list[Task]:
        with self.uow.transaction():
            tasks = self.uow.project_repository.get_tasks(project_id)

        return tasks
