from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from web.pages.base_page import BasePage


class SideMenu(BasePage):
    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    MENU_WRAP = (By.CSS_SELECTOR, ".bm-menu-wrap")

    def open(self) -> "SideMenu":
        self.js_click(self.BURGER_BUTTON)
        self.wait.until(ec.element_to_be_clickable(self.LOGOUT_LINK))
        return self

    def logout(self) -> None:
        self.js_click(self.LOGOUT_LINK)
        self.wait_for_url("saucedemo.com/")
