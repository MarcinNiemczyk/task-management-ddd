from typing import Annotated

from fastapi import Depends

from src.domain.ports.unit_of_work import IUnitOfWork
from src.infrastructure.database.unit_of_work import UnitOfWork


def get_unit_of_work() -> IUnitOfWork:
    return UnitOfWork()


UoWDependency = Annotated[IUnitOfWork, Depends(get_unit_of_work)]
