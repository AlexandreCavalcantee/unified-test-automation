import pytest

from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage
from web.pages.side_menu import SideMenu

pytestmark = pytest.mark.web


class TestLogout:
    def test_logout_via_side_menu_returns_to_login(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")
        InventoryPage(driver).loaded()

        SideMenu(driver).open().logout()

        assert "saucedemo.com" in driver.current_url
        assert "inventory.html" not in driver.current_url
