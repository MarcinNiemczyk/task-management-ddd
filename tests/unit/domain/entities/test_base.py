from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.base import BaseEntity


class TestBaseEntity:
    def test_create_entity_with_defaults(self):
        entity = BaseEntity()

        assert entity.id is not None
        assert isinstance(entity.id, UUID)
        assert entity.created_at is not None
        assert isinstance(entity.created_at, datetime)
        assert entity.updated_at is not None
        assert isinstance(entity.updated_at, datetime)
        assert entity.created_at == entity.updated_at

    def test_create_entity_with_custom_id(self, fixed_uuid):
        entity = BaseEntity(id=fixed_uuid)

        assert entity.id == fixed_uuid

    def test_create_entity_with_custom_timestamps(self, fixed_uuid, fixed_datetime):
        created = fixed_datetime
        updated = datetime(2025, 11, 16, 12, 0, 0, tzinfo=timezone.utc)

        entity = BaseEntity(
            id=fixed_uuid,
            created_at=created,
            updated_at=updated,
        )

        assert entity.id == fixed_uuid
        assert entity.created_at == created
        assert entity.updated_at == updated

    def test_timestamps_are_timezone_aware(self):
        entity = BaseEntity()

        assert entity.created_at.tzinfo is not None
        assert entity.updated_at.tzinfo is not None
        assert entity.created_at.tzinfo == timezone.utc
        assert entity.updated_at.tzinfo == timezone.utc

    def test_multiple_entities_have_unique_ids(self):
        entity1 = BaseEntity()
        entity2 = BaseEntity()
        entity3 = BaseEntity()

        assert entity1.id != entity2.id
        assert entity2.id != entity3.id
        assert entity1.id != entity3.id

    def test_get_current_time_returns_utc(self):
        current_time = BaseEntity._get_current_time()

        assert isinstance(current_time, datetime)
        assert current_time.tzinfo == timezone.utc

    def test_created_at_only_custom(self, fixed_datetime):
        entity = BaseEntity(created_at=fixed_datetime)

        assert entity.created_at == fixed_datetime
        assert entity.updated_at is not None
        # updated_at should be auto-generated (now)
        assert entity.updated_at >= entity.created_at

    def test_updated_at_only_custom(self, fixed_datetime):
        entity = BaseEntity(updated_at=fixed_datetime)

        assert entity.updated_at == fixed_datetime
        assert entity.created_at is not None
