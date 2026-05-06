from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from web.pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
    INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    INVENTORY_ITEM_IMG = (By.CSS_SELECTOR, ".inventory_item_img img")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

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
        self.js_click(self._add_button_for(item_name))
        self.present(self._remove_button_for(item_name))
        return self

    def remove_from_cart(self, item_name: str) -> "InventoryPage":
        self.js_click(self._remove_button_for(item_name))
        self.present(self._add_button_for(item_name))
        return self

    def cart_count(self) -> int:
        return int(self.text_of(self.CART_BADGE))

    def has_cart_badge(self) -> bool:
        return len(self.driver.find_elements(*self.CART_BADGE)) > 0

    def open_cart(self) -> None:
        self.js_click(self.CART_LINK)
        self.wait_for_url("cart.html")

    def sort_by(self, value: str) -> "InventoryPage":
        select = Select(self.visible(self.SORT_DROPDOWN))
        select.select_by_value(value)
        return self

    def item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self.INVENTORY_ITEM_NAME)]

    def item_prices(self) -> list[float]:
        return [
            float(el.text.replace("$", ""))
            for el in self.driver.find_elements(*self.INVENTORY_ITEM_PRICE)
        ]

    def item_image_sources(self) -> list[str]:
        self.wait.until(ec.presence_of_all_elements_located(self.INVENTORY_ITEM_IMG))
        return [
            el.get_attribute("src")
            for el in self.driver.find_elements(*self.INVENTORY_ITEM_IMG)
        ]
