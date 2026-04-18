from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class SearchPage(BasePage):

    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".thumbnail")

    def sort_by_name_asc(self):
        select = Select(self.find_element(self.SORT_DROPDOWN))
        select.select_by_visible_text("Name A - Z")

    def get_products_count(self):
        return len(self.find_elements(self.PRODUCT_ITEMS))
