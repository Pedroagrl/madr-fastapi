import pytest
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from madr.models import table_registry
from madr.app import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        
    table_registry.metadata.drop_all(engine)