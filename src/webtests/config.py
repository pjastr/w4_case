"""Page URLs and browser settings.

Defaults point to the public pages; every value can be overridden with an
environment variable (PyCharm: Run ▸ Edit Configurations ▸ Environment variables),
so changing the environment never requires changing the code.
"""
import os

INTERNET_URL = os.getenv("INTERNET_URL", "https://the-internet.herokuapp.com").rstrip("/")
SELENIUM_WEB_URL = os.getenv("SELENIUM_WEB_URL", "https://www.selenium.dev/selenium/web").rstrip("/")

HEADLESS = os.getenv("HEADLESS", "0") == "1"          # HEADLESS=1 – no browser window
WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1280,900")     # the layout depends on it
TIMEOUT = float(os.getenv("TIMEOUT", "10"))            # max wait in seconds
