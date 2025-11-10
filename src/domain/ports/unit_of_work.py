from abc import ABC, abstractmethod
from typing import Any

from src.domain.ports.repositories.project_repository import IProjectRepository
from src.domain.ports.repositories.task_repository import ITaskRepository


class IUnitOfWork(ABC):
    @abstractmethod
    def transaction(self) -> Any:
        pass

    @property
    @abstractmethod
    def task_repository(self) -> ITaskRepository:
        pass

    @property
    @abstractmethod
    def project_repository(self) -> IProjectRepository:
        pass
