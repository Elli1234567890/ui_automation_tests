import allure
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.home_page import HomePage
from pages.category_page import CategoryPage


@allure.epic("UI Automation Tests")
@allure.feature("Интернет-магазин automationteststore.com")
class TestStore:

    @allure.title("TЗ-1: Фильтрация в категориях")
    @allure.description("Проверка сортировки товаров по имени и цене")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filtering(self, driver, base_url):
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)

        with allure.step("Открыть главную страницу"):
            home_page.open(base_url)

        with allure.step("Перейти в категорию Apparel & Accessories"):
            home_page.go_to_category("Apparel")

        with allure.step("Выбрать подкатегорию Shoes"):
            home_page.go_to_category("Apparel")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".thumbnail")))

        with allure.step("Сортировка по имени A-Z"):
            category_page.select_sort_option("Name A - Z")
            time.sleep(2)
            names = category_page.get_product_names()
            assert len(names) >= 4, "Ожидалось минимум 4 товара"
            assert category_page.is_sorted_ascending(names), "Имена не отсортированы A-Z"

        with allure.step("Сортировка по имени Z-A"):
            category_page.select_sort_option("Name Z - A")
            time.sleep(2)
            names = category_page.get_product_names()
            assert category_page.is_sorted_descending(names), "Имена не отсортированы Z-A"

        with allure.step("Сортировка по цене Low > High"):
            category_page.select_sort_option("Price Low > High")
            time.sleep(2)
            prices = category_page.get_product_prices()
            assert len(prices) >= 4, "Ожидалось минимум 4 цены"
            assert category_page.is_sorted_ascending(prices), "Цены не отсортированы Low-High"

        with allure.step("Сортировка по цене High > Low"):
            category_page.select_sort_option("Price High > Low")
            time.sleep(2)
            prices = category_page.get_product_prices()
            assert category_page.is_sorted_descending(prices), "Цены не отсортированы High-Low"

    @allure.title("TЗ-2: Поиск и корзина")
    @allure.description("Поиск shirt, добавление 2 и 3 товара, удвоение самого дешёвого")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_and_cart(self, driver, base_url):
        home_page = HomePage(driver)

        def add_product_by_index(index, quantity):
            driver.get(base_url)
            home_page.search("shirt")
            time.sleep(3)
            
            select = Select(driver.find_element(By.ID, "sort"))
            select.select_by_visible_text("Name A - Z")
            time.sleep(2)
            
            product_links = driver.find_elements(By.CSS_SELECTOR, ".prdocutname")
            if index >= len(product_links):
                return False
            
            product_links[index].click()
            time.sleep(2)
            
            qty_input = driver.find_element(By.ID, "product_quantity")
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            
            add_btn = driver.find_element(By.CSS_SELECTOR, ".cart")
            add_btn.click()
            time.sleep(2)
            
            return True

        with allure.step("Добавить 2-й товар с рандомным количеством"):
            quantity_2 = random.randint(1, 3)
            add_product_by_index(1, quantity_2)

        with allure.step("Добавить 3-й товар с рандомным количеством"):
            quantity_3 = random.randint(1, 3)
            add_product_by_index(2, quantity_3)

        with allure.step("Перейти в корзину"):
            driver.get(base_url)
            home_page.go_to_cart()
            time.sleep(3)

        with allure.step("Найти самый дешёвый товар и удвоить его количество"):
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
            
            cheapest_idx = 0
            cheapest_price = float('inf')
            for idx, row in enumerate(product_rows):
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 4:
                    price_text = cells[3].text.replace("$", "").replace(",", "")
                    if price_text:
                        price = float(price_text)
                        if price < cheapest_price:
                            cheapest_price = price
                            cheapest_idx = idx

            old_total_elem = driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
            old_total_text = old_total_elem.text.replace("$", "").replace(",", "")
            old_total = float(old_total_text) if old_total_text else 0
            print(f"Старая сумма: ${old_total:.2f}")

            cheapest_row = product_rows[cheapest_idx]
            qty_input = cheapest_row.find_element(By.CSS_SELECTOR, "input[type='text']")
            current_qty = int(qty_input.get_attribute("value"))
            new_qty = current_qty * 2
            qty_input.clear()
            qty_input.send_keys(str(new_qty))

            update_btn = driver.find_element(By.ID, "cart_update")
            update_btn.click()
            time.sleep(3)

            new_total_elem = driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
            new_total_text = new_total_elem.text.replace("$", "").replace(",", "")
            new_total = float(new_total_text) if new_total_text else 0
            print(f"Новая сумма: ${new_total:.2f}")

            assert new_total != old_total, f"Сумма не изменилась: было ${old_total:.2f}, стало ${new_total:.2f}"

        with allure.step("Проверить итоговую сумму"):
            total_elem = driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
            total_text = total_elem.text.replace("$", "").replace(",", "")
            total = float(total_text) if total_text else 0
            assert total > 0, f"Итоговая сумма должна быть больше 0, получено {total}"
            print(f"\nИтоговая сумма после удвоения: ${total:.2f}")

    @allure.title("TЗ-3: Проверка корзины")
    @allure.description("Добавление товаров и удаление чётных позиций")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_operations(self, driver, base_url):
        home_page = HomePage(driver)

        def add_product_from_home(index, quantity):
            driver.get(base_url)
            time.sleep(2)
            
            product_links = driver.find_elements(By.CSS_SELECTOR, ".prdocutname")
            if index >= len(product_links):
                return False
            
            product_links[index].click()
            time.sleep(2)
            
            qty_input = driver.find_element(By.ID, "product_quantity")
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            
            add_btn = driver.find_element(By.CSS_SELECTOR, ".cart")
            add_btn.click()
            time.sleep(2)
            
            return True

        with allure.step("Добавить 5 случайных товаров с главной страницы"):
            driver.get(base_url)
            product_count = len(driver.find_elements(By.CSS_SELECTOR, ".prdocutname"))
            assert product_count >= 5, f"Недостаточно товаров: {product_count}"
            
            selected = random.sample(range(product_count), 5)
            for idx in selected:
                quantity = random.randint(1, 3)
                add_product_from_home(idx, quantity)

        with allure.step("Перейти в корзину"):
            driver.get(base_url)
            home_page.go_to_cart()
            time.sleep(3)

        with allure.step("Удалить все чётные по порядку товары"):
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
            
            for idx in [3, 1]:
                if idx < len(product_rows):
                    remove_btn = product_rows[idx].find_element(By.CSS_SELECTOR, "td:last-child a")
                    remove_btn.click()
                    time.sleep(2)
                    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
                    product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]

        with allure.step("Проверить итоговую сумму"):
            total_elem = driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
            total_text = total_elem.text.replace("$", "").replace(",", "")
            total = float(total_text) if total_text else 0
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
            print(f"\nОсталось товаров: {len(product_rows)}, сумма: ${total:.2f}")
            assert total > 0, "Итоговая сумма должна быть больше 0"
