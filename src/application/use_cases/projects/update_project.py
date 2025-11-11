from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.entities.project import Project
from src.domain.ports.unit_of_work import IUnitOfWork


@dataclass
class UpdateProjectCommand:
    title: str | None
    deadline: str | None


class UpdateProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self, project_id: UUID, command: UpdateProjectCommand) -> Project:
        with self.uow.transaction():
            project = self.uow.project_repository.get(project_id)

            if command.title is not None:
                project.update_title(command.title)

            if command.deadline is not None:
                project.update_deadline(datetime.fromisoformat(command.deadline))

            updated_project = self.uow.project_repository.update(project)

        return updated_project
