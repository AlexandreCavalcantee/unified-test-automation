import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


def build_driver(headless: bool = True) -> WebDriver:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    binary = os.getenv("BROWSER_BINARY")
    if binary:
        options.binary_location = binary

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    return driver
