"""Lecture 4, slide "Opcje przeglądarki (Options)" – headless Chrome.

Run: right-click ▸ Run 'browser_options' (or: python examples/browser_options.py).
No window opens – the title is printed in the Run panel.
"""
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")        # no window
options.add_argument("--window-size=1280,800")
options.add_argument("--lang=pl")
options.page_load_strategy = "normal"         # eager, none
driver = webdriver.Chrome(options=options)

driver.get("https://the-internet.herokuapp.com/login")
print(driver.title)                           # The Internet
print(driver.get_window_size())               # {'width': 1280, 'height': 800}
driver.quit()
