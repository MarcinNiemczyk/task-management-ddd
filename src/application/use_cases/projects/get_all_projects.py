from src.domain.entities.project import Project
from src.domain.ports.unit_of_work import IUnitOfWork


class GetAllProjectsUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    def execute(self) -> list[Project]:
        with self.uow.transaction():
            projects = self.uow.project_repository.get_all()

        return projects
