from src.application.ports.event_publisher import IEventPublisher
from src.domain.events.project_deadline_shortened import ProjectDeadlineShortened
from src.infrastructure.celery.handlers import handle_project_deadline_shortened_task


class EventPublisher(IEventPublisher):
    def publish(self, events: list[object]):
        for event in events:
            match event:
                case ProjectDeadlineShortened() as evt:
                    handle_project_deadline_shortened_task.delay(evt.to_dict())
