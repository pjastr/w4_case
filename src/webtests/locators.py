"""Locators as constants in ONE place (slide "Dobre praktyki lokalizatorów").

When the page changes, only this file needs updating – not every test.
Priority: id ▸ name ▸ short CSS ▸ XPath only for text or axes.
The classes are just namespaces; full Page Objects come in lecture 9.
"""
from selenium.webdriver.common.by import By


class LoginPage:
    PATH = "/login"
    FORM = (By.ID, "login")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "#login button")
    FLASH = (By.ID, "flash")
    LOGOUT = (By.LINK_TEXT, "Logout")


class TablesPage:
    PATH = "/tables"
    TABLE1 = (By.ID, "table1")
    TABLE1_ROWS = (By.CSS_SELECTOR, "#table1 tbody tr")


class AddRemovePage:
    PATH = "/add_remove_elements/"
    ADD = (By.CSS_SELECTOR, ".example > button")
    DELETE = (By.CSS_SELECTOR, "#elements button")


class InputsPage:
    PATH = "/inputs"
    NUMBER = (By.CSS_SELECTOR, "input[type=number]")


class DropdownPage:
    PATH = "/dropdown"
    DROPDOWN = (By.ID, "dropdown")


class CheckboxesPage:
    PATH = "/checkboxes"
    FORM = (By.ID, "checkboxes")


class WebFormPage:
    PATH = "/web-form.html"
    FORM = (By.TAG_NAME, "form")
    TEXT = (By.ID, "my-text-id")
    TEXTAREA = (By.NAME, "my-textarea")
    SUBMIT = (By.TAG_NAME, "button")
    RETURN_LINK = (By.LINK_TEXT, "Return to index")
    MESSAGE = (By.ID, "message")
