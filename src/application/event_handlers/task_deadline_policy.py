from src.application.ports.unit_of_work import IUnitOfWork
from src.domain.events.project_deadline_shortened import \
    ProjectDeadlineShortened


class TaskDeadlinePolicyHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def handle(self, event: ProjectDeadlineShortened):
        with self.uow.transaction():
            tasks_to_update = self.uow.project_repository.get_tasks(event.project_id)
            for task in tasks_to_update:
                task.update_deadline(event.new_deadline)
