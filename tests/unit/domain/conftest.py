from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.entities.project import Project
from src.domain.entities.task import Task


@pytest.fixture
def fixed_uuid():
    return uuid4()


@pytest.fixture
def fixed_datetime():
    return datetime(2025, 11, 15, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def future_datetime():
    return datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


@pytest.fixture
def past_datetime():
    return datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_task(fixed_uuid, future_datetime):
    return Task(
        id=fixed_uuid,
        title="Sample Task",
        description="This is a sample task",
        deadline=future_datetime,
        completed=False,
    )


@pytest.fixture
def sample_project(fixed_uuid, future_datetime):
    return Project(
        id=fixed_uuid,
        title="Sample Project",
        deadline=future_datetime,
        completed=False,
    )


@pytest.fixture
def completed_task(future_datetime):
    return Task(
        title="Completed Task",
        description="This task is done",
        deadline=future_datetime,
        completed=True,
    )


@pytest.fixture
def task_without_description(future_datetime):
    return Task(
        title="Task without description",
        deadline=future_datetime,
    )


@pytest.fixture
def task_with_project(fixed_uuid, future_datetime):
    project_id = uuid4()
    return Task(
        id=fixed_uuid,
        title="Task with project",
        description="Belongs to a project",
        deadline=future_datetime,
        project_id=project_id,
    )
