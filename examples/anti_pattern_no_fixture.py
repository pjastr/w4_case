"""Lecture 4, slide "Test w pytest – bez fixture" – an ANTI-PATTERN, kept for comparison.

Problems: the URL is hard-coded, Chrome()/quit() would be repeated in every test,
and when the assert fails, quit() never runs – the browser stays open.
The right way: the `driver` fixture in tests/conftest.py.

Not collected by default (outside testpaths); run it on purpose:
    python -m pytest examples/anti_pattern_no_fixture.py
"""
from selenium import webdriver


def test_title():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")
    assert driver.title == "The Internet"
    driver.quit()          # never runs if the assert fails!
