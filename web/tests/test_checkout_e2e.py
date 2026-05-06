import pytest

from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


class TestCheckout:
    def test_full_checkout_flow_succeeds(self, driver):
        login = LoginPage(driver).open()
        login.login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver).loaded()
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.add_to_cart("Sauce Labs Bike Light")
        assert inventory.cart_count() == 2

        inventory.open_cart()
        cart = CartPage(driver).loaded()
        items = cart.item_names()
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items
        cart.checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_info("Alex", "Cavalcante", "01310-100")
        checkout.finish()

        assert "Thank you for your order" in checkout.success_message()

    def test_login_with_locked_user_shows_error(self, driver):
        login = LoginPage(driver).open()
        login.login("locked_out_user", "secret_sauce")

        assert "locked out" in login.error_message().lower()

    def test_login_with_invalid_credentials_shows_error(self, driver):
        login = LoginPage(driver).open()
        login.login("standard_user", "wrong_password")

        assert "username and password do not match" in login.error_message().lower()
