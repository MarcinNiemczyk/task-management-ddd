from contextlib import contextmanager
from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from src.application.ports.repositories.project_repository import \
    IProjectRepository
from src.application.ports.repositories.task_repository import ITaskRepository
from src.application.ports.unit_of_work import IUnitOfWork
from src.domain.entities.project import Project
from src.domain.entities.task import Task
from src.domain.exceptions.base import EntityNotFoundException


class MockTaskRepository(ITaskRepository):
    def __init__(self):
        self.tasks: dict[UUID, Task] = {}
        self.add_mock = MagicMock(side_effect=self._add)
        self.get_mock = MagicMock(side_effect=self._get)
        self.update_mock = MagicMock(side_effect=self._update)
        self.delete_mock = MagicMock(side_effect=self._delete)
        self.get_all_mock = MagicMock(side_effect=self._get_all)
        self.get_by_project_mock = MagicMock(side_effect=self._get_by_project)

    def _add(self, task: Task) -> Task:
        self.tasks[task.id] = task
        return task

    def _get(self, task_id: UUID) -> Task:
        task = self.tasks.get(task_id)
        if not task:
            raise EntityNotFoundException("Task", task_id)
        return task

    def _update(self, task: Task) -> Task:
        if task.id not in self.tasks:
            raise EntityNotFoundException("Task", task.id)
        self.tasks[task.id] = task
        return task

    def _delete(self, task_id: UUID) -> None:
        if task_id not in self.tasks:
            raise EntityNotFoundException("Task", task_id)
        del self.tasks[task_id]

    def _get_all(
        self,
        completed: bool | None = None,
        overdue: bool | None = None,
        project_id: UUID | None = None,
    ) -> list[Task]:
        tasks = list(self.tasks.values())

        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        if project_id is not None:
            tasks = [t for t in tasks if t.project_id == project_id]

        if overdue is not None:
            now = datetime.now(timezone.utc)
            if overdue:
                tasks = [t for t in tasks if t.deadline < now and not t.completed]
            else:
                tasks = [t for t in tasks if t.deadline >= now or t.completed]

        return tasks

    def _get_by_project(self, project_id: UUID) -> list[Task]:
        return [task for task in self.tasks.values() if task.project_id == project_id]

    def add(self, task: Task) -> Task:
        return self.add_mock(task)

    def get(self, task_id: UUID) -> Task:
        return self.get_mock(task_id)

    def update(self, task: Task) -> Task:
        return self.update_mock(task)

    def delete(self, task_id: UUID) -> None:
        return self.delete_mock(task_id)

    def get_all(
        self,
        completed: bool | None = None,
        overdue: bool | None = None,
        project_id: UUID | None = None,
    ) -> list[Task]:
        return self.get_all_mock(
            completed=completed, overdue=overdue, project_id=project_id
        )

    def get_by_project(self, project_id: UUID) -> list[Task]:
        return self.get_by_project_mock(project_id)


class MockProjectRepository(IProjectRepository):
    def __init__(self):
        self.projects: dict[UUID, Project] = {}
        self.get_mock = MagicMock(side_effect=self._get)
        self.add_mock = MagicMock(side_effect=self._add)
        self.update_mock = MagicMock(side_effect=self._update)
        self.delete_mock = MagicMock(side_effect=self._delete)
        self.get_all_mock = MagicMock(side_effect=self._get_all)
        self.delete_project_tasks_mock = MagicMock(
            side_effect=self._delete_project_tasks
        )
        self.count_open_tasks_mock = MagicMock(side_effect=self._count_open_tasks)
        self.get_tasks_mock = MagicMock(side_effect=self._get_tasks)

    def _get(self, project_id: UUID) -> Project:
        project = self.projects.get(project_id)
        if not project:
            raise EntityNotFoundException("Project", project_id)
        return project

    def _add(self, project: Project) -> Project:
        self.projects[project.id] = project
        return project

    def _update(self, project: Project) -> Project:
        if project.id not in self.projects:
            raise EntityNotFoundException("Project", project.id)
        self.projects[project.id] = project
        return project

    def _delete(self, project_id: UUID) -> None:
        if project_id not in self.projects:
            raise EntityNotFoundException("Project", project_id)
        del self.projects[project_id]

    def _get_all(self) -> list[Project]:
        return list(self.projects.values())

    def _delete_project_tasks(self, project_id: UUID) -> None:
        # Mock implementation - in real scenario would cascade delete tasks
        pass

    def _count_open_tasks(self, project_id: UUID) -> int:
        # Mock implementation - returns 0 by default
        return 0

    def _get_tasks(self, project_id: UUID) -> list[Task]:
        # Mock implementation - returns empty list by default
        return []

    def get(self, project_id: UUID) -> Project:
        return self.get_mock(project_id)

    def add(self, project: Project) -> Project:
        return self.add_mock(project)

    def update(self, project: Project) -> Project:
        return self.update_mock(project)

    def delete(self, project_id: UUID) -> None:
        return self.delete_mock(project_id)

    def get_all(self) -> list[Project]:
        return self.get_all_mock()

    def delete_project_tasks(self, project_id: UUID) -> None:
        return self.delete_project_tasks_mock(project_id)

    def count_open_tasks(self, project_id: UUID) -> int:
        return self.count_open_tasks_mock(project_id)

    def get_tasks(self, project_id: UUID) -> list[Task]:
        return self.get_tasks_mock(project_id)

    def add_project(self, project: Project) -> None:
        """Helper method for test setup"""
        self.projects[project.id] = project


class MockUnitOfWork(IUnitOfWork):
    def __init__(self):
        self._task_repository = MockTaskRepository()
        self._project_repository = MockProjectRepository()
        self._in_transaction = False

    @contextmanager
    def transaction(self):
        self._in_transaction = True
        try:
            yield
        finally:
            self._in_transaction = False

    @property
    def task_repository(self) -> ITaskRepository:
        return self._task_repository

    @property
    def project_repository(self) -> IProjectRepository:
        return self._project_repository


@pytest.fixture
def mock_uow():
    return MockUnitOfWork()


@pytest.fixture
def sample_project_for_task():
    return Project(
        id=uuid4(),
        title="Test Project",
        deadline=datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
        completed=False,
    )


@pytest.fixture
def project_with_early_deadline():
    return Project(
        id=uuid4(),
        title="Project with Early Deadline",
        deadline=datetime(2025, 11, 30, 23, 59, 59, tzinfo=timezone.utc),
        completed=False,
    )
