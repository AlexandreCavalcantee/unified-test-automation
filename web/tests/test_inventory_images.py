import pytest

from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage

pytestmark = pytest.mark.web


class TestInventoryImages:
    def test_standard_user_sees_unique_product_images(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver).loaded()

        sources = inventory.item_image_sources()
        assert len(sources) == 6
        assert len(set(sources)) == len(sources), (
            f"expected all images unique, got duplicates: {sources}"
        )

    def test_problem_user_exposes_duplicate_image_bug(self, driver):
        LoginPage(driver).open().login("problem_user", "secret_sauce")
        inventory = InventoryPage(driver).loaded()

        sources = inventory.item_image_sources()
        assert len(set(sources)) < len(sources), (
            "problem_user is expected to render duplicate images — "
            "if this passes, the SauceDemo bug fixture changed"
        )
