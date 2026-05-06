from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator) -> WebElement:
        return self.wait.until(ec.visibility_of_element_located(locator))

    def present(self, locator) -> WebElement:
        return self.wait.until(ec.presence_of_element_located(locator))

    def clickable(self, locator) -> WebElement:
        return self.wait.until(ec.element_to_be_clickable(locator))

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(ec.url_contains(fragment))

    def click(self, locator) -> None:
        element = self.clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.visible(locator).text
