from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    @staticmethod
    def _add_button_for(item_name: str) -> tuple:
        slug = item_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{slug}")

    def loaded(self) -> "InventoryPage":
        self.visible(self.INVENTORY_LIST)
        return self

    def add_to_cart(self, item_name: str) -> "InventoryPage":
        self.click(self._add_button_for(item_name))
        return self

    def cart_count(self) -> int:
        return int(self.text_of(self.CART_BADGE))

    def open_cart(self) -> None:
        self.click(self.CART_LINK)
        self.wait_for_url("/cart.html")
