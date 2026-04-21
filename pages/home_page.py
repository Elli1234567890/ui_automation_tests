from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    CATEGORY_LINKS = (By.CSS_SELECTOR, ".nav-pills.categorymenu li a")
    CART_LINK = (By.CSS_SELECTOR, ".topcart li a")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "filter_keyword"))
        )

    def search(self, keyword):
        self.input_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".thumbnail"))
        )

    def go_to_category(self, category_name):
        categories = self.find_elements(self.CATEGORY_LINKS)
        for category in categories:
            if category_name.lower() in category.text.lower():
                category.click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".thumbnail"))
                )
                return True
        raise AssertionError(f"Категория '{category_name}' не найдена")

    def go_to_cart(self):
        self.click(self.CART_LINK)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )