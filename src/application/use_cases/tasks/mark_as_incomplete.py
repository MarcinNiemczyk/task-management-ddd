from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


class MarkTaskAsIncompleteUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, task_id: UUID) -> Task:
        with self.uow.transaction():
            task = self.uow.task_repository.get(task_id)

            task.mark_as_incomplete()
            updated_task = self.uow.task_repository.update(task)

            if task.project_id:
                has_any_open_tasks = (
                    self.uow.project_repository.count_open_tasks(task.project_id) > 0
                )
                if not has_any_open_tasks:
                    project = self.uow.project_repository.get(task.project_id)
                    if project.completed:
                        project.mark_as_incomplete()
                        _ = self.uow.project_repository.update(project)

        return updated_task

