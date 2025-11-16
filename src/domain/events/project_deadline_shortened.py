from dataclasses import asdict, dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ProjectDeadlineShortened:
    project_id: UUID
    new_deadline: datetime

    def to_dict(self):
        return asdict(self)
