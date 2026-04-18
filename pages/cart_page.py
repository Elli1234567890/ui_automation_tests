from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    CART_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "td:nth-child(4)")
    PRODUCT_TOTAL = (By.CSS_SELECTOR, "td:nth-child(6)")
    REMOVE_BTN = (By.CSS_SELECTOR, "td:nth-child(7) a")
    TOTAL_AMOUNT = (By.CSS_SELECTOR, ".total")

    def get_cart_items(self):
        rows = self.find_elements(self.CART_ROWS)
        items = []
        for idx, row in enumerate(rows):
            try:
                price_text = row.find_element(*self.PRODUCT_PRICE).text
                price = float(price_text.replace("$", "").replace(",", ""))
                total_text = row.find_element(*self.PRODUCT_TOTAL).text
                total = float(total_text.replace("$", "").replace(",", ""))
                quantity = int(total / price) if price > 0 else 1
                items.append({
                    "index": idx,
                    "price": price,
                    "quantity": quantity,
                    "total": total
                })
            except:
                continue
        return items

    def remove_item(self, item_index):
        rows = self.find_elements(self.CART_ROWS)
        if item_index < len(rows):
            remove_btn = rows[item_index].find_element(*self.REMOVE_BTN)
            remove_btn.click()

    def get_total_amount(self):
        total_elem = self.find_element(self.TOTAL_AMOUNT)
        total_text = total_elem.text.replace("$", "").replace(",", "")
        return float(total_text) if total_text else 0.0

    def find_cheapest_item(self, items):
        return min(items, key=lambda x: x["price"]) if items else None
