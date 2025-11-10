from uuid import UUID


class DomainException(Exception):
    pass


class EntityNotFoundException(DomainException):
    def __init__(self, entity_type: str, entity_id: UUID):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with ID {entity_id} not found")
