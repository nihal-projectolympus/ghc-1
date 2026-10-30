import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    snapshot = copy.deepcopy(activities)
    yield
    # Endpoints hold a reference to this dict, so restore it in place.
    activities.clear()
    activities.update(snapshot)
