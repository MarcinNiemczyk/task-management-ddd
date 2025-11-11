from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


class GetTaskUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, task_id: UUID) -> Task:
        with self.uow.transaction():
            task = self.uow.task_repository.get(task_id)

        return task
