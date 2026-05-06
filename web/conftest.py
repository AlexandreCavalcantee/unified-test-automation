import os

import pytest

from web.utils.driver_factory import build_driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def driver(request):
    headless = os.getenv("HEADLESS", "true").lower() != "false"
    instance = build_driver(headless=headless)
    yield instance
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        os.makedirs("screenshots", exist_ok=True)
        name = request.node.name.replace("/", "_")
        instance.save_screenshot(f"screenshots/{name}.png")
        print(f"\n[debug] url={instance.current_url}")
        print(f"[debug] title={instance.title}")
    instance.quit()
