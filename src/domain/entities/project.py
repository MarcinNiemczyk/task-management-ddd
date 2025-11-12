from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.base import BaseEntity


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

    def update_title(self, title: str) -> None:
        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def update_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_completed(self) -> None:
        self.completed = True
        self.updated_at = datetime.now(timezone.utc)
