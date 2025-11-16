from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.project import Project
from src.domain.entities.task import Task


class IProjectRepository(ABC):
    @abstractmethod
    def add(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get(self, project_id: UUID) -> Project:
        pass

    @abstractmethod
    def get_all(self) -> list[Project]:
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        pass

    @abstractmethod
    def delete(self, project_id: UUID) -> None:
        pass

    @abstractmethod
    def delete_project_tasks(self, project_id: UUID) -> None:
        pass

    @abstractmethod
    def count_open_tasks(self, project_id: UUID) -> int:
        pass

    @abstractmethod
    def get_tasks(self, project_id: UUID) -> list[Task]:
        pass
