"""Lecture 4, slide "Pierwszy skrypt" – a plain script without pytest.

Run: right-click ▸ Run 'first_script' (or: python examples/first_script.py).
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/login")
print(driver.title)                       # The Internet
field = driver.find_element(By.ID, "username")
field.send_keys("tomsmith")
driver.quit()
