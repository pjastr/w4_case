"""Explicit waits used by the tests – never time.sleep().

After navigation we wait for an element characteristic of the page
(a "marker") to be sure we are working on the NEW page.
Explicit waits (WebDriverWait) in detail – lecture 5.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webtests.config import TIMEOUT


def wait_for(driver: WebDriver, *locator: str, timeout: float = TIMEOUT) -> WebElement:
    """Waits until the element is present in the DOM and returns it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator))


def open_page(driver: WebDriver, url: str, *marker: str) -> WebElement:
    """Opens the URL and waits for the page marker; returns the marker."""
    driver.get(url)
    return wait_for(driver, *marker)


def wait_for_fonts(driver: WebDriver, timeout: float = TIMEOUT) -> None:
    """Waits until web fonts are loaded – needed before layout-based
    locators (locate_with), otherwise the page may still move."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.fonts.status") == "loaded")
