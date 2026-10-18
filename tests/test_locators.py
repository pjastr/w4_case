"""Lecture 4, part "Lokalizatory".

These tests are ABOUT locator strategies, so they show the locators inline;
elsewhere the tests take them from webtests/locators.py.
"""
import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from webtests.config import INTERNET_URL
from webtests.locators import AddRemovePage, LoginPage, TablesPage
from webtests.waits import open_page, wait_for_fonts


def test_locator_strategies(driver):
    """Slide "Lokalizatory w kodzie": By.ID, NAME, CSS, TAG_NAME, XPATH."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.NAME, "password")
    button = driver.find_element(By.CSS_SELECTOR, "#login button")
    heading = driver.find_element(By.TAG_NAME, "h2")
    label = driver.find_element(By.XPATH, "//label[text()='Password']")

    assert driver.find_element(*LoginPage.USERNAME) == username  # tuple + *
    assert password.get_dom_attribute("type") == "password"
    assert button.get_dom_attribute("type") == "submit"
    assert heading.text == "Login Page"
    assert label.get_dom_attribute("for") == "password"


def test_xpath_table(driver):
    """Slide "XPath – przykład: tabela"."""
    open_page(driver, f"{INTERNET_URL}{TablesPage.PATH}", *TablesPage.TABLE1)

    xp = "//table[@id='table1']//td[.='Doe']/following-sibling::td[2]"
    email = driver.find_element(By.XPATH, xp).text
    row = driver.find_element(By.XPATH, "//td[.='Doe']/..")
    amount = row.find_element(By.XPATH, "./td[4]").text

    assert email == "jdoe@hotmail.com"
    assert amount == "$100.00"
    # the console shows (2) [tr, tr]: Doe is in BOTH tables – find_element takes the first
    assert len(driver.find_elements(By.XPATH, "//td[.='Doe']/..")) == 2


def test_relative_locators(driver):
    """Slide "Lokalizatory względne": they use the LAYOUT, so wait for fonts first."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    wait_for_fonts(driver)

    password = driver.find_element(
        locate_with(By.TAG_NAME, "input").below({By.ID: "username"}))
    label = driver.find_element(
        locate_with(By.TAG_NAME, "label").above({By.ID: "password"}))

    assert password.get_dom_attribute("id") == "password"
    assert label.text == "Password"


def test_find_elements_returns_empty_list(driver):
    """Slide "find_element a find_elements": no match -> [] (no exception)."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    assert driver.find_elements(*LoginPage.FLASH) == []


def test_search_in_element_context(driver):
    """Slide "Wyszukiwanie w kontekście elementu"."""
    table = open_page(driver, f"{INTERNET_URL}{TablesPage.PATH}", *TablesPage.TABLE1)

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    first = rows[0]
    cells = first.find_elements(By.TAG_NAME, "td")
    email = first.find_element(By.XPATH, "./td[3]").text   # dot = from this element

    assert len(rows) == 4
    assert cells[0].text == "Smith"
    assert email == "jsmith@gmail.com"


def test_stale_element(driver):
    """Slide "Element „nieświeży” (stale)": search again after the DOM changes."""
    add = open_page(driver, f"{INTERNET_URL}{AddRemovePage.PATH}", *AddRemovePage.ADD)
    add.click()
    delete = driver.find_element(*AddRemovePage.DELETE)

    delete.click()                     # the element leaves the DOM

    with pytest.raises(StaleElementReferenceException):
        delete.click()                 # stale reference
