from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.project import Project


class ProjectCreateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Project title",
        examples=["Q4 Marketing Campaign"],
    )
    deadline: str = Field(
        description="Project deadline in ISO 8601 format",
        examples=["2025-12-31T23:59:59Z"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Q4 Marketing Campaign",
                "deadline": "2025-12-31T23:59:59Z",
            }
        }
    )


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    deadline: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Q4 Marketing Campaign",
                "deadline": "2025-12-31T23:59:59Z",
            }
        },
    )

    @classmethod
    def from_entity(cls, project: Project) -> "ProjectResponse":
        return cls(
            id=project.id,
            title=project.title,
            deadline=project.deadline,
        )


class ProjectUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Project title",
        examples=["Q4 Marketing Campaign"],
    )
    deadline: str | None = Field(
        default=None,
        description="Project deadline in ISO 8601 format",
        examples=["2025-12-31T23:59:59Z"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Q4 Marketing Campaign",
                "deadline": "2025-12-31T23:59:59Z",
            }
        }
    )
