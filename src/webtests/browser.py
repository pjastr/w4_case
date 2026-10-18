"""One place that creates the browser – tests never call webdriver.Chrome() directly."""
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from webtests.config import HEADLESS, WINDOW_SIZE


def create_driver(headless: bool = HEADLESS) -> WebDriver:
    """Starts Chrome with the same options for every test.

    Selenium Manager downloads a matching chromedriver – no admin rights needed.
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)   # explicit waits only (see waits.py)
    return driver
