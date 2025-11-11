from uuid import UUID

from src.domain.ports.unit_of_work import IUnitOfWork


class DeleteTaskUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, task_id: UUID) -> None:
        with self.uow.transaction():
            self.uow.task_repository.delete(task_id)
