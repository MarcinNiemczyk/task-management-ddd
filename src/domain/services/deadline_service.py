from datetime import timezone
from src.domain.exceptions.task_exceptions import (
    TaskDeadlineExceedsProjectDeadlineException,
)
from src.domain.entities.project import Project
from src.domain.entities.task import Task


class DeadlineValidationService:
    def ensure_task_deadline_within_project(self, task: Task, project: Project):
        if task.deadline and project.deadline:
            task_deadline = (
                task.deadline
                if task.deadline.tzinfo
                else task.deadline.replace(tzinfo=timezone.utc)
            )
            project_deadline = (
                project.deadline
                if project.deadline.tzinfo
                else project.deadline.replace(tzinfo=timezone.utc)
            )

            if task_deadline > project_deadline:
                raise TaskDeadlineExceedsProjectDeadlineException(
                    task.deadline, project.deadline
                )
