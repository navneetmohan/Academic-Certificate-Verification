import pytest
from app.database.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    init_db()
    yield
