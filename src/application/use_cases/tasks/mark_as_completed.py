from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.config_port import ConfigPort
from src.domain.ports.unit_of_work import IUnitOfWork


class MarkTaskAsCompletedUseCase:
    def __init__(self, uow: IUnitOfWork, config: ConfigPort) -> None:
        self.uow = uow
        self.config = config

    def execute(self, task_id: UUID) -> Task:
        with self.uow.transaction():
            task = self.uow.task_repository.get(task_id)

            task.mark_as_completed()
            updated_task = self.uow.task_repository.update(task)

            if task.project_id:
                has_other_open_tasks = (
                    self.uow.project_repository.count_open_tasks(task.project_id) > 1
                )
                auto_complete_project = (
                    self.config.auto_complete_project_on_last_task_done()
                )
                if not has_other_open_tasks and auto_complete_project:
                    project = self.uow.project_repository.get(task.project_id)
                    project.mark_as_completed()
                    _ = self.uow.project_repository.update(project)

        return updated_task
