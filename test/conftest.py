import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from enumTest2.main import app
from enumTest2.db import get_session

# Use in-memory SQLite for testing
test_engine = create_engine("sqlite:///:memory:")

# Override dependency
def override_get_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    app.dependency_overrides[get_session] = override_get_session
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture()
def client():
    return TestClient(app)