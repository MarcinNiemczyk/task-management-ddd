from sqlalchemy.orm import relationship

from src.domain.entities.task import Task
from src.domain.entities.project import Project
from src.infrastructure.database.tables.task_table import tasks
from src.infrastructure.database.tables.project_table import projects
from src.infrastructure.database.config import mapper_registry


def start_mappers() -> None:
    mapper_registry.map_imperatively(
        Project,
        projects,
    )

    mapper_registry.map_imperatively(
        Task,
        tasks,
        properties={
            "project": relationship(
                Project,
                backref="tasks",
                foreign_keys=[tasks.c.project_id],
            ),
        },
    )
