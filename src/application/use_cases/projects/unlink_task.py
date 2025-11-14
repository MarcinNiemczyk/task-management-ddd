from uuid import UUID

from src.domain.exceptions.task_exceptions import TaskNotLinkedToProjectException
from src.domain.ports.unit_of_work import IUnitOfWork


class UnlinkTaskFromProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, project_id: UUID, task_id: UUID) -> None:
        with self.uow.transaction():
            self.uow.project_repository.get(project_id)

            task = self.uow.task_repository.get(task_id)

            if task.project_id != project_id:
                raise TaskNotLinkedToProjectException(task_id, project_id)

            task.project_id = None
            self.uow.task_repository.update(task)
