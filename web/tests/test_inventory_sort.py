import pytest

from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


def _login_as_standard(driver) -> InventoryPage:
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    return InventoryPage(driver).loaded()


class TestInventorySort:
    def test_sort_name_a_to_z(self, driver):
        inventory = _login_as_standard(driver)
        inventory.sort_by("az")

        names = inventory.item_names()
        assert names == sorted(names)

    def test_sort_name_z_to_a(self, driver):
        inventory = _login_as_standard(driver)
        inventory.sort_by("za")

        names = inventory.item_names()
        assert names == sorted(names, reverse=True)

    def test_sort_price_low_to_high(self, driver):
        inventory = _login_as_standard(driver)
        inventory.sort_by("lohi")

        prices = inventory.item_prices()
        assert prices == sorted(prices)

    def test_sort_price_high_to_low(self, driver):
        inventory = _login_as_standard(driver)
        inventory.sort_by("hilo")

        prices = inventory.item_prices()
        assert prices == sorted(prices, reverse=True)
