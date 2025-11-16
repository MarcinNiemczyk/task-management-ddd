from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.application.use_cases.tasks.create_task import (CreateTaskCommand,
                                                         CreateTaskUseCase)
from src.domain.exceptions.base import EntityNotFoundException
from src.domain.exceptions.task_exceptions import \
    TaskDeadlineExceedsProjectDeadlineException


class TestCreateTaskUseCase:

    def test_create_task_without_project(self, mock_uow):
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Standalone Task",
            description="This task is not linked to any project",
            deadline="2025-12-31T23:59:59+00:00",
            project_id=None,
        )

        result = use_case.execute(command)

        assert result is not None
        assert result.title == "Standalone Task"
        assert result.description == "This task is not linked to any project"
        assert result.deadline == datetime(
            2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc
        )
        assert result.project_id is None
        assert result.completed is False

        mock_uow.task_repository.add_mock.assert_called_once()
        mock_uow.project_repository.get_mock.assert_not_called()

    def test_create_task_with_valid_project(self, mock_uow, sample_project_for_task):
        mock_uow.project_repository.add_project(sample_project_for_task)
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Project Task",
            description="Task within project deadline",
            deadline="2025-12-30T23:59:59+00:00",
            project_id=sample_project_for_task.id,
        )

        result = use_case.execute(command)

        assert result is not None
        assert result.title == "Project Task"
        assert result.project_id == sample_project_for_task.id
        assert result.deadline == datetime(
            2025, 12, 30, 23, 59, 59, tzinfo=timezone.utc
        )

        mock_uow.task_repository.add_mock.assert_called_once()
        mock_uow.project_repository.get_mock.assert_called_once_with(
            sample_project_for_task.id
        )

    def test_create_task_with_deadline_exceeding_project_deadline(
        self, mock_uow, project_with_early_deadline
    ):
        mock_uow.project_repository.add_project(project_with_early_deadline)
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Task with Invalid Deadline",
            description="This task's deadline exceeds project deadline",
            deadline="2025-12-31T23:59:59+00:00",  # After project deadline (Nov 30)
            project_id=project_with_early_deadline.id,
        )

        with pytest.raises(TaskDeadlineExceedsProjectDeadlineException) as exc_info:
            use_case.execute(command)

        assert exc_info.value.task_deadline == datetime(
            2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc
        )
        assert exc_info.value.project_deadline == project_with_early_deadline.deadline

        mock_uow.project_repository.get_mock.assert_called_once()
        mock_uow.task_repository.add_mock.assert_not_called()

    def test_create_task_with_nonexistent_project(self, mock_uow):
        use_case = CreateTaskUseCase(mock_uow)
        nonexistent_project_id = uuid4()
        command = CreateTaskCommand(
            title="Task with Invalid Project",
            description="Project does not exist",
            deadline="2025-12-31T23:59:59+00:00",
            project_id=nonexistent_project_id,
        )

        with pytest.raises(EntityNotFoundException) as exc_info:
            use_case.execute(command)

        assert exc_info.value.entity_type == "Project"
        assert exc_info.value.entity_id == nonexistent_project_id

        mock_uow.project_repository.get_mock.assert_called_once_with(
            nonexistent_project_id
        )
        mock_uow.task_repository.add_mock.assert_not_called()

    def test_create_task_without_description(self, mock_uow):
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Task Without Description",
            description=None,
            deadline="2025-12-31T23:59:59+00:00",
            project_id=None,
        )

        result = use_case.execute(command)

        assert result is not None
        assert result.title == "Task Without Description"
        assert result.description is None
        assert result.deadline == datetime(
            2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc
        )

        mock_uow.task_repository.add_mock.assert_called_once()

    def test_create_task_with_same_deadline_as_project(
        self, mock_uow, sample_project_for_task
    ):
        mock_uow.project_repository.add_project(sample_project_for_task)
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Task at Boundary",
            description="Task deadline equals project deadline",
            deadline=sample_project_for_task.deadline.isoformat(),
            project_id=sample_project_for_task.id,
        )

        result = use_case.execute(command)

        assert result is not None
        assert result.project_id == sample_project_for_task.id
        assert result.deadline == sample_project_for_task.deadline

        mock_uow.task_repository.add_mock.assert_called_once()
        mock_uow.project_repository.get_mock.assert_called_once()

    def test_task_id_is_generated(self, mock_uow):
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Task with Generated ID",
            description="Should have UUID",
            deadline="2025-12-31T23:59:59+00:00",
            project_id=None,
        )

        result = use_case.execute(command)

        assert result.id is not None
        assert isinstance(result.id, type(uuid4()))

    def test_created_task_has_timestamps(self, mock_uow):
        use_case = CreateTaskUseCase(mock_uow)
        command = CreateTaskCommand(
            title="Task with Timestamps",
            description="Should have timestamps",
            deadline="2025-12-31T23:59:59+00:00",
            project_id=None,
        )

        result = use_case.execute(command)

        assert result.created_at is not None
        assert result.updated_at is not None
        assert result.created_at.tzinfo == timezone.utc
        assert result.updated_at.tzinfo == timezone.utc
