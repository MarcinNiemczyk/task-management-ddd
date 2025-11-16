import pytest
from celery import Celery
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.api.main import app
from src.infrastructure.database.config import get_session, mapper_registry


@pytest.fixture
def test_db():
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    mapper_registry.metadata.create_all(bind=test_engine)
    
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=test_engine
    )
    
    db = TestSessionLocal()
    yield db
    
    db.close()
    mapper_registry.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(test_db):
    def override_get_session():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

