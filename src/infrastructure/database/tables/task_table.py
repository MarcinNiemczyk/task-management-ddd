from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, String, Table, UUID
from src.infrastructure.database.config import mapper_registry


def utcnow():
    return datetime.now(timezone.utc)


tasks = Table(
    "tasks",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("description", String(1000), nullable=True),
    Column("deadline", DateTime, nullable=False),
    Column("completed", Boolean, default=False, nullable=False),
    Column(
        "project_id",
        UUID,
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("created_at", DateTime, default=utcnow, nullable=False),
    Column("updated_at", DateTime, default=utcnow, onupdate=utcnow, nullable=False),
    Index("ix_tasks_completed", "completed"),
    Index("ix_tasks_deadline", "deadline"),
    Index("ix_tasks_project_id", "project_id"),
)
