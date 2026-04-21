from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CategoryPage(BasePage):

    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".price .oneprice")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".prdocutname")

    def open_subcategory_shoes(self):
        self.driver.get("https://automationteststore.com/index.php?rt=product/category&path=68")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".thumbnail"))
        )

    def select_sort_option(self, option_text):
        select = Select(self.find_element(self.SORT_DROPDOWN))
        select.select_by_visible_text(option_text)
        WebDriverWait(self.driver, 5).until(
            lambda d: len(self.get_product_names()) >= 4
        )

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