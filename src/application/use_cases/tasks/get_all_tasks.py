from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


class GetAllTasksUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        completed: bool | None = None,
        overdue: bool | None = None,
        project_id: UUID | None = None,
    ) -> list[Task]:
        with self.uow.transaction():
            tasks = self.uow.task_repository.get_all(
                completed=completed,
                overdue=overdue,
                project_id=project_id,
            )

        return tasks
