from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
    SUCCESS_HEADER = (By.CSS_SELECTOR, ".complete-header")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first: str, last: str, postal: str) -> "CheckoutPage":
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.js_click(self.CONTINUE_BUTTON)
        self.wait_for_url("checkout-step-two.html")
        return self

    def submit_info(self, first: str, last: str, postal: str) -> "CheckoutPage":
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.js_click(self.CONTINUE_BUTTON)
        return self

    def finish(self) -> None:
        self.js_click(self.FINISH_BUTTON)
        self.wait_for_url("checkout-complete.html")

    def cancel(self) -> None:
        self.js_click(self.CANCEL_BUTTON)

    def success_message(self) -> str:
        return self.text_of(self.SUCCESS_HEADER)

    def error_message(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)
