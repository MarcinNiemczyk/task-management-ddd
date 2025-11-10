from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get(self, task_id: UUID) -> Task:
        pass

    @abstractmethod
    def get_all(
        self,
        completed: bool | None = None,
        overdue: bool | None = None,
        project_id: UUID | None = None,
    ) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_project(self, project_id: UUID) -> list[Task]:
        pass
