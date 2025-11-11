from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.entities.project import Project
from src.domain.ports.unit_of_work import IUnitOfWork


@dataclass
class CreateProjectCommand:
    title: str
    deadline: str


class CreateProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, command: CreateProjectCommand) -> Project:
        project = Project(
            id=uuid4(),
            title=command.title,
            deadline=datetime.fromisoformat(command.deadline),
        )

        with self.uow.transaction():
            created_project = self.uow.project_repository.add(project)

        return created_project
