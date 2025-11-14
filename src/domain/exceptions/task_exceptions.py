from src.domain.exceptions.base import DomainException


class TaskDeadlineExceedsProjectDeadlineException(DomainException):
    def __init__(self, task_deadline, project_deadline):
        self.task_deadline = task_deadline
        self.project_deadline = project_deadline
        super().__init__(
            f"Task deadline {task_deadline} exceeds project deadline {project_deadline}"
        )


class TaskNotLinkedToProjectException(DomainException):
    def __init__(self, task_id, project_id):
        self.task_id = task_id
        self.project_id = project_id
        super().__init__(
            f"Task {task_id} is not linked to project {project_id}"
        )
