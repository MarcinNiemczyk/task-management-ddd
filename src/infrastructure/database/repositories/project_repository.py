from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.project import Project
from src.domain.entities.task import Task
from src.domain.exceptions.base import EntityNotFoundException
from src.domain.ports.repositories.project_repository import IProjectRepository


class ProjectRepository(IProjectRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, project: Project) -> Project:
        self._session.add(project)
        return project

    def get(self, project_id: UUID) -> Project:
        project = self._session.query(Project).filter(Project.id == project_id).first()

        if project is None:
            raise EntityNotFoundException("Project", project_id)

        return project

    def get_all(self) -> list[Project]:
        return self._session.query(Project).all()

    def update(self, project: Project) -> Project:
        existing = self._session.query(Project).filter(Project.id == project.id).first()
        if existing is None:
            raise EntityNotFoundException("Project", project.id)

        updated_project = self._session.merge(project)

        return updated_project

    def delete(self, project_id: UUID) -> None:
        project = self._session.query(Project).filter(Project.id == project_id).first()

        if project is None:
            raise EntityNotFoundException("Project", project_id)

        self._session.delete(project)

    def delete_project_tasks(self, project_id: UUID) -> None:
        self._session.query(Task).filter(Task.project_id == project_id).delete()

    def count_open_tasks(self, project_id: UUID) -> int:
        return (
            self._session.query(Task)
            .filter(Task.project_id == project_id, Task.completed == False)
            .count()
        )

    def get_tasks(self, project_id: UUID) -> list[Task]:
        return (
            self._session.query(Task)
            .filter(Task.project_id == project_id)
            .all()
        )
