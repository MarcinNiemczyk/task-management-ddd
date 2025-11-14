from uuid import UUID

from src.domain.ports.unit_of_work import IUnitOfWork
from src.domain.services.deadline_service import DeadlineValidationService


class LinkTaskToProjectUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow
        self.deadline_service = DeadlineValidationService()

    def execute(self, project_id: UUID, task_id: UUID) -> None:
        with self.uow.transaction():
            project = self.uow.project_repository.get(project_id)
            task = self.uow.task_repository.get(task_id)

            self.deadline_service.ensure_task_deadline_within_project(task, project)

            task.project_id = project_id
            self.uow.task_repository.update(task)

            # If task is not completed and project is completed, mark project as incomplete
            if not task.completed and project.completed:
                project.mark_as_incomplete()
                self.uow.project_repository.update(project)
