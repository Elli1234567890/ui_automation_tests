from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class CategoryPage(BasePage):

    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".price .oneprice")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".prdocutname")

    def select_sort_option(self, option_text):
        select = Select(self.find_element(self.SORT_DROPDOWN))
        select.select_by_visible_text(option_text)

    def get_product_prices(self):
        elements = self.find_elements(self.PRODUCT_PRICES)
        prices = []
        for el in elements:
            text = el.text.replace("$", "").replace(",", "")
            if text:
                prices.append(float(text))
        return prices

    def get_product_names(self):
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements if el.text]

    @staticmethod
    def is_sorted_ascending(items):
        return all(items[i] <= items[i + 1] for i in range(len(items) - 1))

    @staticmethod
    def is_sorted_descending(items):
        return all(items[i] >= items[i + 1] for i in range(len(items) - 1))
