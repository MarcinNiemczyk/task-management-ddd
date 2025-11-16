from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.base import BaseEntity
from src.domain.events.project_deadline_shortened import \
    ProjectDeadlineShortened


class Project(BaseEntity):
    def __init__(
        self,
        title: str,
        deadline: datetime,
        completed: bool = False,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(id, created_at, updated_at)
        self.title = title
        self.deadline = deadline
        self.completed = completed
        self._domain_events: list[object] = []

    @property
    def domain_events(self) -> list[object]:
        if not hasattr(self, '_domain_events'):
            self._domain_events = []
        return self._domain_events

    def update_title(self, title: str) -> None:
        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def update_deadline(self, deadline: datetime) -> None:
        new_deadline = deadline if deadline.tzinfo else deadline.replace(tzinfo=timezone.utc)
        current_deadline = self.deadline if self.deadline.tzinfo else self.deadline.replace(tzinfo=timezone.utc)
        if new_deadline < current_deadline:
            if not hasattr(self, '_domain_events'):
                self._domain_events = []
            event = ProjectDeadlineShortened(
                project_id=self.id, new_deadline=new_deadline
            )
            self._domain_events.append(event)
        self.deadline = new_deadline
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_completed(self) -> None:
        self.completed = True
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_incomplete(self) -> None:
        self.completed = False
        self.updated_at = datetime.now(timezone.utc)

    def clear_domain_events(self):
        self._domain_events.clear()
