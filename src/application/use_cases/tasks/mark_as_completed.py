from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


@dataclass
class MarkTaskAsCompletedCommand:
    completed: bool


class MarkTaskAsCompletedUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, task_id: UUID, command: MarkTaskAsCompletedCommand) -> Task:
        with self.uow.transaction():
            task = self.uow.task_repository.get(task_id)

            if command.completed:
                task.mark_as_completed()
            else:
                task.mark_as_incomplete()

            updated_task = self.uow.task_repository.update(task)

        return updated_task
