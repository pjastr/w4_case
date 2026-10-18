"""Lecture 4, part "Interakcje z elementami".

Each test follows Arrange – Act – Assert and checks ONE behaviour;
locators come from webtests/locators.py, URLs from webtests/config.py.
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from webtests.config import INTERNET_URL, SELENIUM_WEB_URL
from webtests.locators import (
    CheckboxesPage, DropdownPage, InputsPage, LoginPage, WebFormPage)
from webtests.waits import open_page, wait_for


def log_in(driver, username, password):
    """Fills in the login form and returns the #flash message."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    driver.find_element(*LoginPage.USERNAME).send_keys(username)
    driver.find_element(*LoginPage.PASSWORD).send_keys(password)
    driver.find_element(*LoginPage.SUBMIT).click()
    return wait_for(driver, *LoginPage.FLASH)


def test_send_keys_appends_and_clear_empties(driver):
    """Slide "click, send_keys, clear, submit"."""
    # Arrange
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    username = driver.find_element(*LoginPage.USERNAME)
    # Act
    username.send_keys("tom")
    username.send_keys("smith")        # appends text
    appended = username.get_property("value")
    username.clear()                   # clears the field
    # Assert
    assert appended == "tomsmith"
    assert username.get_property("value") == ""


def test_valid_login_shows_message_and_logout(driver):
    """Slides "click, send_keys…" and "Odczyt: tekst i znacznik"."""
    flash = log_in(driver, "tomsmith", "SuperSecretPassword!")

    assert "You logged into a secure area!" in flash.text   # "contains" – robust
    assert flash.text == "You logged into a secure area!\n×"
    assert flash.tag_name == "div"
    assert len(driver.find_elements(*LoginPage.LOGOUT)) == 1


def test_arrow_keys_and_select_all(driver):
    """Slide "Klawisze specjalne" – number field."""
    field = open_page(driver, f"{INTERNET_URL}{InputsPage.PATH}", *InputsPage.NUMBER)

    field.send_keys("5", Keys.ARROW_UP, Keys.ARROW_UP)   # -> 7
    after_arrows = field.get_property("value")
    field.send_keys(Keys.CONTROL, "a")                   # select all
    field.send_keys(Keys.BACKSPACE)                      # delete

    assert after_arrows == "7"
    assert field.get_property("value") == ""


def test_enter_in_textarea_adds_new_line(driver):
    """Slide "Klawisze specjalne" – Web Form textarea."""
    open_page(driver, f"{SELENIUM_WEB_URL}{WebFormPage.PATH}", *WebFormPage.FORM)
    textarea = driver.find_element(*WebFormPage.TEXTAREA)

    textarea.send_keys("Line 1", Keys.ENTER, "Line 2")

    assert textarea.get_property("value") == "Line 1\nLine 2"


def test_attribute_vs_property(driver):
    """Slide "Atrybut a właściwość – przykład" (Web Form)."""
    open_page(driver, f"{SELENIUM_WEB_URL}{WebFormPage.PATH}", *WebFormPage.FORM)
    text = driver.find_element(*WebFormPage.TEXT)
    link = driver.find_element(*WebFormPage.RETURN_LINK)

    text.send_keys("abc")

    assert text.get_dom_attribute("value") is None     # not in the HTML
    assert text.get_property("value") == "abc"         # current state
    assert text.get_attribute("value") == "abc"        # "smart" read
    assert text.get_dom_attribute("myprop") == "myvalue"
    assert text.get_property("myprop") is None         # not a property
    assert link.get_dom_attribute("href") == "./index.html"
    assert link.get_property("href").endswith("/index.html")   # full URL


def test_button_css_and_geometry(driver, tmp_path):
    """Slide "CSS i geometria elementu"."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    button = driver.find_element(*LoginPage.SUBMIT)

    color = button.value_of_css_property("background-color")
    saved = button.screenshot(str(tmp_path / "button.png"))   # tmp_path – no clutter

    assert color == "rgba(25, 35, 25, 1)"   # new look since 10.2026 (before: blue)
    assert set(button.rect) == {"x", "y", "width", "height"}
    assert button.size["width"] > 0
    assert saved


def test_select_option(driver):
    """Slide "Listy rozwijane – klasa Select"."""
    element = open_page(driver, f"{INTERNET_URL}{DropdownPage.PATH}", *DropdownPage.DROPDOWN)
    dropdown = Select(element)

    dropdown.select_by_visible_text("Option 1")
    dropdown.select_by_value("2")
    dropdown.select_by_index(1)

    assert dropdown.first_selected_option.text == "Option 1"
    assert [o.text for o in dropdown.options] == [
        "Please select an option", "Option 1", "Option 2"]


def test_back_forward_refresh(driver):
    """Slide "Nawigacja"."""
    open_page(driver, f"{INTERNET_URL}{LoginPage.PATH}", *LoginPage.FORM)
    open_page(driver, f"{INTERNET_URL}{CheckboxesPage.PATH}", *CheckboxesPage.FORM)

    driver.back()
    wait_for(driver, *LoginPage.FORM)
    after_back = driver.current_url
    driver.forward()
    wait_for(driver, *CheckboxesPage.FORM)
    driver.refresh()

    assert after_back.endswith(LoginPage.PATH)
    assert driver.current_url.endswith(CheckboxesPage.PATH)
    assert driver.title == "The Internet"


def test_submit_web_form(driver):
    """Slide "Kompletny test – Web Form"."""
    open_page(driver, f"{SELENIUM_WEB_URL}{WebFormPage.PATH}", *WebFormPage.FORM)
    driver.find_element(*WebFormPage.TEXT).send_keys("Selenium")

    driver.find_element(*WebFormPage.SUBMIT).click()

    message = wait_for(driver, *WebFormPage.MESSAGE)
    assert message.text == "Received!"
    assert driver.title == "Web form - target page"
    assert "my-text=Selenium" in driver.current_url
