from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from web.pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CSS_SELECTOR, ".cart_list")
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    @staticmethod
    def _slug(item_name: str) -> str:
        return item_name.lower().replace(" ", "-")

    def _remove_button_for(self, item_name: str) -> tuple:
        return (By.ID, f"remove-{self._slug(item_name)}")

    def loaded(self) -> "CartPage":
        self.present(self.CART_LIST)
        return self

    def item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAME)]

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def remove(self, item_name: str) -> "CartPage":
        button = self._remove_button_for(item_name)
        self.js_click(button)
        self.wait.until(ec.invisibility_of_element_located(button))
        return self

    def checkout(self) -> None:
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_for_url("checkout-step-one.html")
