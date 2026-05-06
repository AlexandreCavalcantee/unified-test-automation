import time

import pytest

from api.client import PetstoreClient


@pytest.fixture(scope="session")
def client() -> PetstoreClient:
    return PetstoreClient()


@pytest.fixture
def unique_id() -> int:
    return int(time.time() * 1000)
