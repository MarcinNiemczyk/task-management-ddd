from datetime import datetime, timezone
from uuid import UUID, uuid4


class BaseEntity:
    @classmethod
    def _get_current_time(cls) -> datetime:
        return datetime.now(timezone.utc)

    def __init__(
        self,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id: UUID = id if id is not None else uuid4()
        now = self._get_current_time()
        self.created_at = created_at if created_at is not None else now
        self.updated_at = updated_at if updated_at is not None else now
