from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.entities.task import Task
from src.domain.ports.unit_of_work import IUnitOfWork


@dataclass
class CreateTaskCommand:
    title: str
    description: str | None
    deadline: str
    project_id: UUID | None = None


class CreateTaskUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, command: CreateTaskCommand) -> Task:
        task = Task(
            id=uuid4(),
            title=command.title,
            description=command.description,
            deadline=datetime.fromisoformat(command.deadline),
        )
        with self.uow.transaction():
            created_task = self.uow.task_repository.add(task)
            
        return created_task
