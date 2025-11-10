from datetime import datetime
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
