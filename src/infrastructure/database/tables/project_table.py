from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, Index, String,
                        Table, UUID)

from src.infrastructure.database.config import mapper_registry


def utcnow():
    return datetime.now(timezone.utc)


projects = Table(
    "projects",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("deadline", DateTime, nullable=False),
    Column("completed", Boolean, default=False, nullable=False),
    Column("created_at", DateTime, default=utcnow, nullable=False),
    Column("updated_at", DateTime, default=utcnow, onupdate=utcnow, nullable=False),
    Index("ix_projects_completed", "completed"),
    Index("ix_projects_deadline", "deadline"),
)
