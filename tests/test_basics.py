"""Lecture 4, part "Pierwszy skrypt i pytest".

The fixture `driver` comes from tests/conftest.py, the URL from config.
"""
from webtests.config import INTERNET_URL
from webtests.locators import LoginPage
from webtests.waits import open_page


def test_title(driver):
    """Slides "Fixture z yield" and "Adresy w konfiguracji"."""
    driver.get(f"{INTERNET_URL}{LoginPage.PATH}")
    assert driver.title == "The Internet"


def test_title_after_page_marker(driver):
    """Slide "Czekanie na znacznik strony": wait for the page, then check it."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    assert driver.title == "The Internet"
    assert driver.current_url.endswith(LoginPage.PATH)
