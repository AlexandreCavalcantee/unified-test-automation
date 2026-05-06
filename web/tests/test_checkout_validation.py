import pytest

from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


def _go_to_checkout_step_one(driver) -> CheckoutPage:
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver).loaded()
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.open_cart()
    CartPage(driver).loaded().checkout()
    return CheckoutPage(driver)


class TestCheckoutValidation:
    def test_continue_without_first_name_shows_error(self, driver):
        checkout = _go_to_checkout_step_one(driver)
        checkout.submit_info("", "Cavalcante", "01310-100")

        assert "First Name is required" in checkout.error_message()

    def test_continue_without_last_name_shows_error(self, driver):
        checkout = _go_to_checkout_step_one(driver)
        checkout.submit_info("Alex", "", "01310-100")

        assert "Last Name is required" in checkout.error_message()

    def test_continue_without_postal_code_shows_error(self, driver):
        checkout = _go_to_checkout_step_one(driver)
        checkout.submit_info("Alex", "Cavalcante", "")

        assert "Postal Code is required" in checkout.error_message()

    def test_cancel_on_step_one_returns_to_cart(self, driver):
        checkout = _go_to_checkout_step_one(driver)
        checkout.cancel()

        assert "cart.html" in driver.current_url
