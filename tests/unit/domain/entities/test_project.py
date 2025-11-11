from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.project import Project


class TestProjectEntity:
    def test_create_project_with_required_fields(self, future_datetime):
        project = Project(
            title="Test Project",
            deadline=future_datetime,
        )

        assert project.title == "Test Project"
        assert project.deadline == future_datetime
        assert project.completed is False
        assert isinstance(project.id, UUID)
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)

    def test_create_project_with_all_fields(
        self, fixed_uuid, fixed_datetime, future_datetime
    ):
        created = fixed_datetime
        updated = datetime(2025, 11, 16, 12, 0, 0, tzinfo=timezone.utc)

        project = Project(
            id=fixed_uuid,
            title="Complete Project",
            deadline=future_datetime,
            completed=True,
            created_at=created,
            updated_at=updated,
        )

        assert project.id == fixed_uuid
        assert project.title == "Complete Project"
        assert project.deadline == future_datetime
        assert project.completed is True
        assert project.created_at == created
        assert project.updated_at == updated

    def test_project_inherits_from_base_entity(self, sample_project):
        assert hasattr(sample_project, "id")
        assert hasattr(sample_project, "created_at")
        assert hasattr(sample_project, "updated_at")
        assert isinstance(sample_project.id, UUID)
        assert isinstance(sample_project.created_at, datetime)
        assert isinstance(sample_project.updated_at, datetime)

    def test_project_not_completed_by_default(self, future_datetime):
        project = Project(
            title="New Project",
            deadline=future_datetime,
        )

        assert project.completed is False

    def test_project_can_be_created_completed(self, future_datetime):
        project = Project(
            title="Completed Project",
            deadline=future_datetime,
            completed=True,
        )

        assert project.completed is True

    def test_project_title_attribute(self, sample_project):
        assert sample_project.title == "Sample Project"

        sample_project.title = "Updated Project Title"
        assert sample_project.title == "Updated Project Title"

    def test_project_deadline_attribute(self, sample_project, future_datetime):
        assert sample_project.deadline == future_datetime

        new_deadline = datetime(2026, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        sample_project.deadline = new_deadline
        assert sample_project.deadline == new_deadline

    def test_project_completed_status_can_change(self, sample_project):
        assert sample_project.completed is False

        sample_project.completed = True
        assert sample_project.completed is True

        sample_project.completed = False
        assert sample_project.completed is False

    def test_multiple_projects_have_unique_ids(self, future_datetime):
        project1 = Project(title="Project 1", deadline=future_datetime)
        project2 = Project(title="Project 2", deadline=future_datetime)
        project3 = Project(title="Project 3", deadline=future_datetime)

        assert project1.id != project2.id
        assert project2.id != project3.id
        assert project1.id != project3.id

    def test_project_with_empty_string_title(self, future_datetime):
        project = Project(title="", deadline=future_datetime)
        assert project.title == ""

    def test_project_timestamps_are_timezone_aware(self, future_datetime):
        project = Project(
            title="Test Project",
            deadline=future_datetime,
        )

        assert project.created_at.tzinfo is not None
        assert project.updated_at.tzinfo is not None
        assert project.created_at.tzinfo == timezone.utc
        assert project.updated_at.tzinfo == timezone.utc

    def test_project_with_past_deadline(self, past_datetime):
        project = Project(
            title="Past Project",
            deadline=past_datetime,
        )

        assert project.deadline == past_datetime
        assert project.deadline < datetime.now(timezone.utc)

    def test_project_equality_by_attributes(self, fixed_uuid, future_datetime):
        project1 = Project(
            id=fixed_uuid,
            title="Same Project",
            deadline=future_datetime,
        )
        project2 = Project(
            id=fixed_uuid,
            title="Same Project",
            deadline=future_datetime,
        )

        assert project1 is not project2

        assert project1.id == project2.id
        assert project1.title == project2.title
        assert project1.deadline == project2.deadline

    def test_update_title_changes_title_and_timestamp(self, sample_project):
        original_updated_at = sample_project.updated_at
        original_title = sample_project.title

        sample_project.update_title("New Project Title")

        assert sample_project.title == "New Project Title"
        assert sample_project.title != original_title
        assert sample_project.updated_at > original_updated_at

    def test_update_deadline_changes_deadline_and_timestamp(self, sample_project):
        original_updated_at = sample_project.updated_at
        new_deadline = datetime(2027, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

        sample_project.update_deadline(new_deadline)

        assert sample_project.deadline == new_deadline
        assert sample_project.updated_at > original_updated_at

    def test_update_title_with_empty_string(self, sample_project):
        sample_project.update_title("")

        assert sample_project.title == ""

    def test_update_methods_preserve_other_attributes(self, sample_project):
        original_id = sample_project.id
        original_created_at = sample_project.created_at
        original_completed = sample_project.completed

        sample_project.update_title("New Title")
        sample_project.update_deadline(
            datetime(2027, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        )

        assert sample_project.id == original_id
        assert sample_project.created_at == original_created_at
        assert sample_project.completed == original_completed
