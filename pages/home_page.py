from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    CATEGORY_LINKS = (By.CSS_SELECTOR, ".nav-pills.categorymenu li a")
    CART_LINK = (By.CSS_SELECTOR, ".topcart li a")

    def search(self, keyword):
        self.input_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def go_to_category(self, category_name):
        categories = self.find_elements(self.CATEGORY_LINKS)
        for category in categories:
            if category_name.lower() in category.text.lower():
                category.click()
                return True
        raise AssertionError(f"Категория '{category_name}' не найдена")

    def go_to_cart(self):
        self.click(self.CART_LINK)
