import pytest

from web.pages.cart_page import CartPage
from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


class TestCart:
    def test_remove_item_from_inventory_clears_badge(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver).loaded()

        inventory.add_to_cart("Sauce Labs Backpack")
        assert inventory.cart_count() == 1

        inventory.remove_from_cart("Sauce Labs Backpack")
        assert not inventory.has_cart_badge()

    def test_remove_item_from_cart_page(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver).loaded()
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.add_to_cart("Sauce Labs Bike Light")
        inventory.open_cart()

        cart = CartPage(driver).loaded()
        assert cart.item_count() == 2

        cart.remove("Sauce Labs Backpack")
        assert "Sauce Labs Backpack" not in cart.item_names()
        assert cart.item_count() == 1
