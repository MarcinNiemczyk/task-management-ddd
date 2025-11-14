from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.task import Task


class TaskCreateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title",
        examples=["Buy groceries"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description",
        examples=["Buy milk, bread, and eggs from the store"],
    )
    deadline: str = Field(
        description="Task deadline in ISO 8601 format",
        examples=["2025-12-31T23:59:59Z"],
    )
    project_id: UUID | None = Field(
        default=None,
        description="Optional project ID to link task to",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "deadline": "2025-11-15T18:00:00Z",
                "project_id": None,
            }
        }
    )


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    deadline: datetime
    completed: bool
    project_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "deadline": "2025-11-15T18:00:00Z",
                "completed": False,
                "project_id": None,
                "created_at": "2023-10-10T10:00:00Z",
                "updated_at": "2023-10-10T10:00:00Z",
            }
        },
    )

    @classmethod
    def from_entity(cls, task: Task) -> "TaskResponse":
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            deadline=task.deadline,
            completed=task.completed,
            project_id=task.project_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title",
        examples=["Buy groceries"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description",
        examples=["Buy milk, bread, and eggs from the store"],
    )
    deadline: str | None = Field(
        default=None,
        description="Task deadline in ISO 8601 format",
        examples=["2025-12-31T23:59:59Z"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs",
                "deadline": "2025-11-15T18:00:00Z",
            }
        }
    )


class TaskCompleteRequest(BaseModel):
    completed: bool = Field(
        description="Mark task as completed (true) or incomplete (false)",
        examples=[True],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "completed": True,
            }
        }
    )
