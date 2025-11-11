from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.task import Task
from src.domain.exceptions.base import EntityNotFoundException
from src.domain.ports.repositories.task_repository import ITaskRepository


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, task: Task) -> Task:
        self._session.add(task)
        return task

    def get(self, task_id: UUID) -> Task:
        task = self._session.query(Task).filter(Task.id == task_id).first()

        if task is None:
            raise EntityNotFoundException("Task", task_id)

        return task

    def get_all(
        self,
        completed: bool | None = None,
        overdue: bool | None = None,
        project_id: UUID | None = None,
    ) -> list[Task]:
        query = self._session.query(Task)

        if completed is not None:
            query = query.filter(Task.completed == completed)

        if overdue is not None:
            now = datetime.now(timezone.utc)
            if overdue:
                query = query.filter(Task.deadline < now, Task.completed == False)
            else:
                query = query.filter((Task.deadline >= now) | (Task.completed == True))

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        return query.all()

    def update(self, task: Task) -> Task:
        existing = self._session.query(Task).filter(Task.id == task.id).first()
        if existing is None:
            raise EntityNotFoundException("Task", task.id)

        updated_task = self._session.merge(task)

        return updated_task

    def delete(self, task_id: UUID) -> None:
        task = self._session.query(Task).filter(Task.id == task_id).first()

        if task is None:
            raise EntityNotFoundException("Task", task_id)

        self._session.delete(task)

    def get_by_project(self, project_id: UUID) -> list[Task]:
        return self._session.query(Task).filter(Task.project_id == project_id).all()
