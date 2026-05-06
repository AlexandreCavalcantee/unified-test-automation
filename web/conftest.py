import os

import pytest

from web.utils.driver_factory import build_driver


@pytest.fixture
def driver():
    headless = os.getenv("HEADLESS", "true").lower() != "false"
    instance = build_driver(headless=headless)
    yield instance
    instance.quit()
