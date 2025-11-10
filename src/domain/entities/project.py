from datetime import datetime
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
