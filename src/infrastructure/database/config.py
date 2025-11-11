from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

DATABASE_URL = "sqlite:///./task_management.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

mapper_registry = registry()


def init_db() -> None:
    mapper_registry.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
