from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.entities.task import Task


class TestTaskEntity:

    def test_create_task_with_required_fields(self, future_datetime):
        task = Task(
            title="Test Task",
            deadline=future_datetime,
        )
        
        assert task.title == "Test Task"
        assert task.deadline == future_datetime
        assert task.description is None
        assert task.completed is False
        assert task.project_id is None
        assert isinstance(task.id, UUID)
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self, fixed_uuid, fixed_datetime, future_datetime):
        project_id = uuid4()
        created = fixed_datetime
        updated = datetime(2025, 11, 16, 12, 0, 0, tzinfo=timezone.utc)
        
        task = Task(
            id=fixed_uuid,
            title="Complete Task",
            description="This is a detailed description",
            deadline=future_datetime,
            completed=True,
            project_id=project_id,
            created_at=created,
            updated_at=updated,
        )
        
        assert task.id == fixed_uuid
        assert task.title == "Complete Task"
        assert task.description == "This is a detailed description"
        assert task.deadline == future_datetime
        assert task.completed is True
        assert task.project_id == project_id
        assert task.created_at == created
        assert task.updated_at == updated

    def test_task_inherits_from_base_entity(self, sample_task):
        assert hasattr(sample_task, 'id')
        assert hasattr(sample_task, 'created_at')
        assert hasattr(sample_task, 'updated_at')
        assert isinstance(sample_task.id, UUID)
        assert isinstance(sample_task.created_at, datetime)
        assert isinstance(sample_task.updated_at, datetime)

    def test_task_without_description(self, task_without_description):
        assert task_without_description.title == "Task without description"
        assert task_without_description.description is None

    def test_task_with_description(self, future_datetime):
        task = Task(
            title="Task with description",
            description="Detailed description here",
            deadline=future_datetime,
        )
        
        assert task.description == "Detailed description here"

    def test_task_not_completed_by_default(self, future_datetime):
        task = Task(
            title="New Task",
            deadline=future_datetime,
        )
        
        assert task.completed is False

    def test_task_can_be_created_completed(self, completed_task):
        assert completed_task.completed is True

    def test_task_without_project_id(self, sample_task):
        assert sample_task.project_id is None

    def test_task_with_project_id(self, task_with_project):
        assert task_with_project.project_id is not None
        assert isinstance(task_with_project.project_id, UUID)

    def test_task_title_attribute(self, sample_task):
        assert sample_task.title == "Sample Task"
        
        sample_task.title = "Updated Title"
        assert sample_task.title == "Updated Title"

    def test_task_deadline_attribute(self, sample_task, future_datetime):
        assert sample_task.deadline == future_datetime
        
        new_deadline = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        sample_task.deadline = new_deadline
        assert sample_task.deadline == new_deadline

    def test_task_completed_status_can_change(self, sample_task):
        assert sample_task.completed is False
        
        sample_task.completed = True
        assert sample_task.completed is True
        
        sample_task.completed = False
        assert sample_task.completed is False

    def test_task_description_can_be_updated(self, sample_task):
        assert sample_task.description == "This is a sample task"
        
        sample_task.description = "Updated description"
        assert sample_task.description == "Updated description"
        
        sample_task.description = None
        assert sample_task.description is None

    def test_task_project_id_can_be_assigned(self, sample_task):
        assert sample_task.project_id is None
        
        new_project_id = uuid4()
        sample_task.project_id = new_project_id
        assert sample_task.project_id == new_project_id

    def test_multiple_tasks_have_unique_ids(self, future_datetime):
        task1 = Task(title="Task 1", deadline=future_datetime)
        task2 = Task(title="Task 2", deadline=future_datetime)
        task3 = Task(title="Task 3", deadline=future_datetime)
        
        assert task1.id != task2.id
        assert task2.id != task3.id
        assert task1.id != task3.id

    def test_task_with_empty_string_title(self, future_datetime):
        task = Task(title="", deadline=future_datetime)
        assert task.title == ""

    def test_task_with_empty_string_description(self, future_datetime):
        task = Task(
            title="Task",
            description="",
            deadline=future_datetime,
        )
        assert task.description == ""
