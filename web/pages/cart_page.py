from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def loaded(self) -> "CartPage":
        self.present(self.CART_ITEM)
        return self

    def item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAME)]

    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
