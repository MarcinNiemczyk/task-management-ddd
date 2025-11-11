from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.base import BaseEntity


class Task(BaseEntity):
    def __init__(
        self,
        title: str,
        deadline: datetime,
        description: str | None = None,
        completed: bool = False,
        project_id: UUID | None = None,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(id, created_at, updated_at)
        self.title = title
        self.deadline = deadline
        self.description = description
        self.completed = completed
        self.project_id = project_id

    def mark_as_completed(self) -> None:
        self.completed = True
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_incomplete(self) -> None:
        self.completed = False
        self.updated_at = datetime.now(timezone.utc)

    def update_title(self, title: str) -> None:
        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def update_description(self, description: str | None) -> None:
        self.description = description
        self.updated_at = datetime.now(timezone.utc)

    def update_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline
        self.updated_at = datetime.now(timezone.utc)
