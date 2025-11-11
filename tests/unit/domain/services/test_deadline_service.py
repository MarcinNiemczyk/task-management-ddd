from datetime import datetime, timezone

import pytest

from src.domain.entities.project import Project
from src.domain.entities.task import Task
from src.domain.exceptions.task_exceptions import (
    TaskDeadlineExceedsProjectDeadlineException,
)
from src.domain.services.deadline_service import DeadlineValidationService


class TestDeadlineValidationService:
    @pytest.fixture
    def service(self):
        return DeadlineValidationService()

    def test_task_deadline_before_project_deadline_passes(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        task_deadline = datetime(2025, 12, 15, 12, 0, 0, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_task_deadline_equals_project_deadline_passes(self, service):
        deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=deadline,
        )
        task = Task(
            title="Test Task",
            deadline=deadline,
        )

        # Should not raise exception (equal is acceptable)
        service.ensure_task_deadline_within_project(task, project)

    def test_task_deadline_after_project_deadline_raises_exception(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        task_deadline = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException) as exc_info:
            service.ensure_task_deadline_within_project(task, project)

        assert exc_info.value.task_deadline == task_deadline
        assert exc_info.value.project_deadline == project_deadline

    def test_task_deadline_exceeds_by_one_second_raises_exception(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        task_deadline = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException):
            service.ensure_task_deadline_within_project(task, project)

    def test_naive_datetime_handling_task_exceeds(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59)
        task_deadline = datetime(2026, 1, 15, 12, 0, 0)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException):
            service.ensure_task_deadline_within_project(task, project)

    def test_naive_datetime_handling_task_within(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59)  # naive
        task_deadline = datetime(2025, 12, 15, 12, 0, 0)  # naive

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_mixed_naive_and_aware_datetimes(self, service):
        project_deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        task_deadline = datetime(2025, 12, 15, 12, 0, 0)  # naive

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_task_deadline_way_before_project_deadline(self, service):
        project_deadline = datetime(2025, 12, 31, tzinfo=timezone.utc)
        task_deadline = datetime(2025, 1, 1, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_task_deadline_way_after_project_deadline(self, service):
        project_deadline = datetime(2025, 12, 31, tzinfo=timezone.utc)
        task_deadline = datetime(2026, 12, 31, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException):
            service.ensure_task_deadline_within_project(task, project)

    def test_same_date_different_times_within_deadline(self, service):
        same_date = datetime(2025, 12, 31, tzinfo=timezone.utc)
        project_deadline = same_date.replace(hour=23, minute=59, second=59)
        task_deadline = same_date.replace(hour=10, minute=0, second=0)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_same_date_different_times_exceeds_deadline(self, service):
        same_date = datetime(2025, 12, 31, tzinfo=timezone.utc)
        project_deadline = same_date.replace(hour=10, minute=0, second=0)
        task_deadline = same_date.replace(hour=23, minute=59, second=59)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException):
            service.ensure_task_deadline_within_project(task, project)

    def test_timezone_aware_comparison(self, service):
        project_deadline = datetime(2025, 12, 31, 12, 0, 0, tzinfo=timezone.utc)
        task_deadline = datetime(2025, 12, 31, 11, 0, 0, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        # Should not raise exception
        service.ensure_task_deadline_within_project(task, project)

    def test_service_does_not_modify_entities(self, service):
        project_deadline = datetime(2025, 12, 31, tzinfo=timezone.utc)
        task_deadline = datetime(2025, 12, 15, tzinfo=timezone.utc)

        project = Project(
            title="Test Project",
            deadline=project_deadline,
        )
        task = Task(
            title="Test Task",
            deadline=task_deadline,
        )

        original_task_deadline = task.deadline
        original_project_deadline = project.deadline

        service.ensure_task_deadline_within_project(task, project)

        assert task.deadline == original_task_deadline
        assert project.deadline == original_project_deadline

    def test_multiple_validations_on_same_service_instance(self, service):
        project = Project(
            title="Test Project",
            deadline=datetime(2025, 12, 31, tzinfo=timezone.utc),
        )

        task1 = Task(
            title="Task 1",
            deadline=datetime(2025, 12, 1, tzinfo=timezone.utc),
        )
        task2 = Task(
            title="Task 2",
            deadline=datetime(2025, 12, 15, tzinfo=timezone.utc),
        )

        service.ensure_task_deadline_within_project(task1, project)
        service.ensure_task_deadline_within_project(task2, project)

        task3 = Task(
            title="Task 3",
            deadline=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException):
            service.ensure_task_deadline_within_project(task3, project)
