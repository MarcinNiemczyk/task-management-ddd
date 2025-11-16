from src.application.event_handlers.task_deadline_policy import \
    TaskDeadlinePolicyHandler
from src.domain.events.project_deadline_shortened import ProjectDeadlineShortened

from .app import celery_app


@celery_app.task(name="handle_project_deadline_shortened")
def handle_project_deadline_shortened_task(event_data: dict):
    from src.infrastructure.api.dependencies import get_unit_of_work
    uow = get_unit_of_work()
    handler = TaskDeadlinePolicyHandler(uow)

    event = ProjectDeadlineShortened(**event_data)
    handler.handle(event)
