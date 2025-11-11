from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork
from src.domain.services.deadline_service import DeadlineValidationService


@dataclass
class CreateTaskCommand:
    title: str
    description: str | None
    deadline: str
    project_id: UUID | None = None


class CreateTaskUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow
        self.deadline_service = DeadlineValidationService()

    def execute(self, command: CreateTaskCommand) -> Task:
        task = Task(
            id=uuid4(),
            title=command.title,
            description=command.description,
            deadline=datetime.fromisoformat(command.deadline),
            project_id=command.project_id,
        )
        with self.uow.transaction():
            if command.project_id:
                project = self.uow.project_repository.get(command.project_id)
                self.deadline_service.ensure_task_deadline_within_project(task, project)

            created_task = self.uow.task_repository.add(task)

        return created_task
