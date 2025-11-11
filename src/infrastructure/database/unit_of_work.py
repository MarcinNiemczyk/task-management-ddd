from contextlib import contextmanager
from typing import Generator, Callable

from sqlalchemy.orm import Session

from src.domain.ports.repositories.project_repository import IProjectRepository
from src.domain.ports.repositories.task_repository import ITaskRepository
from src.domain.ports.unit_of_work import IUnitOfWork

from src.infrastructure.database.config import SessionLocal


class UnitOfWork(IUnitOfWork):
    def __init__(
        self,
        task_repository_factory: Callable[[Session], ITaskRepository],
        project_repository_factory: Callable[[Session], IProjectRepository],
    ) -> None:
        self._task_repository_factory = task_repository_factory
        self._project_repository_factory = project_repository_factory

        self._task_repository: ITaskRepository | None = None
        self._project_repository: IProjectRepository | None = None

    @contextmanager
    def transaction(self) -> Generator[None, None, None]:
        session = SessionLocal()
        try:
            self._task_repository = self._task_repository_factory(session)
            self._project_repository = self._project_repository_factory(session)

            yield

            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            self._task_repository = None
            self._project_repository = None

    @property
    def task_repository(self) -> ITaskRepository:
        if self._task_repository is None:
            raise RuntimeError(
                "Task repository accessed outside of transaction context. "
                "Use 'with uow.transaction():' first."
            )
        return self._task_repository

    @property
    def project_repository(self) -> IProjectRepository:
        if self._project_repository is None:
            raise RuntimeError(
                "Project repository accessed outside of transaction context. "
                "Use 'with uow.transaction():' first."
            )
        return self._project_repository
