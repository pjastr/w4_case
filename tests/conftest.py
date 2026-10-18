"""Shared fixtures and hooks for all tests (slides "Fixture z yield", "conftest.py").

pytest finds this file by itself – the tests never import it.
"""
import pytest

from webtests.browser import create_driver


@pytest.fixture
def driver():
    """A new browser for each test (scope="function" – isolated tests)."""
    drv = create_driver()   # setup
    yield drv               # the test runs here
    drv.quit()              # cleanup – also after a failure


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Saves a screenshot of the browser when a test fails.

    The file goes to reports/screenshots/<test name>.png – easier diagnosis.
    """
    report = yield
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            folder = item.config.rootpath / "reports" / "screenshots"
            folder.mkdir(parents=True, exist_ok=True)
            drv.save_screenshot(str(folder / f"{item.name}.png"))
    return report
