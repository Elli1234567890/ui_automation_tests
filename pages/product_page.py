from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    QUANTITY_INPUT = (By.ID, "product_quantity")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".cart")

    def set_quantity(self, quantity):
        qty_input = self.find_element(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(quantity))

    def add_to_cart(self, quantity=1):
        if quantity > 1:
            self.set_quantity(quantity)
        self.click(self.ADD_TO_CART_BTN)
