import pytest
from fastapi.testclient import TestClient

from mma_analytics_hub.main import app  # Adjust the import based on your project structure

@pytest.fixture()
def client():
    """Fixture to create a TestClient for the FastAPI app."""
    return TestClient(app)
