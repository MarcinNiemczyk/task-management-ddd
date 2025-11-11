from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork
from src.domain.services.deadline_service import DeadlineValidationService


@dataclass
class UpdateTaskCommand:
    title: str | None
    description: str | None
    deadline: str | None


class UpdateTaskUseCase:
    def __init__(
        self, uow: IUnitOfWork, deadline_service: DeadlineValidationService
    ) -> None:
        self.uow = uow
        self.deadline_service = deadline_service

    def execute(self, task_id: UUID, command: UpdateTaskCommand) -> Task:
        with self.uow.transaction():
            task = self.uow.task_repository.get(task_id)

            if command.title is not None:
                task.title = command.title

            if command.description is not None:
                task.description = command.description

            if command.deadline is not None:
                if task.project_id is not None:
                    project = self.uow.project_repository.get(task.project_id)
                    self.deadline_service.ensure_task_deadline_within_project(
                        task, project
                    )
                task.deadline = datetime.fromisoformat(command.deadline)

            updated_task = self.uow.task_repository.update(task)

        return updated_task
