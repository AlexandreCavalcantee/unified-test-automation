from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    @staticmethod
    def _slug(item_name: str) -> str:
        return item_name.lower().replace(" ", "-")

    def _add_button_for(self, item_name: str) -> tuple:
        return (By.ID, f"add-to-cart-{self._slug(item_name)}")

    def _remove_button_for(self, item_name: str) -> tuple:
        return (By.ID, f"remove-{self._slug(item_name)}")

    def loaded(self) -> "InventoryPage":
        self.visible(self.INVENTORY_LIST)
        return self

    def add_to_cart(self, item_name: str) -> "InventoryPage":
        self.click(self._add_button_for(item_name))
        self.present(self._remove_button_for(item_name))
        return self

    def cart_count(self) -> int:
        return int(self.text_of(self.CART_BADGE))

    def open_cart(self) -> None:
        link = self.clickable(self.CART_LINK)
        self.driver.execute_script("arguments[0].click();", link)
        self.wait_for_url("cart.html")
