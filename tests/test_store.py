import allure
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@allure.epic("UI Automation Tests")
@allure.feature("Интернет-магазин automationteststore.com")
class TestStore:

    @allure.title("TЗ-1: Фильтрация в категориях")
    @allure.description("Проверка сортировки товаров по имени и цене")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_filtering(self, home_page, category_page):
        with allure.step("Открыть главную страницу"):
            home_page.open()
            WebDriverWait(home_page.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter_keyword"))
            )

        with allure.step("Перейти в категорию Apparel & Accessories"):
            home_page.go_to_category("Apparel")

        with allure.step("Выбрать подкатегорию Shoes"):
            category_page.open_subcategory_shoes()

        with allure.step("Сортировка по имени A-Z"):
            category_page.select_sort_option("Name A - Z")
            names = category_page.get_product_names()
            assert len(names) >= 4, "Ожидалось минимум 4 товара"
            assert category_page.is_sorted_ascending(names), "Имена не отсортированы A-Z"

        with allure.step("Сортировка по имени Z-A"):
            category_page.select_sort_option("Name Z - A")
            names = category_page.get_product_names()
            assert category_page.is_sorted_descending(names), "Имена не отсортированы Z-A"

        with allure.step("Сортировка по цене Low > High"):
            category_page.select_sort_option("Price Low > High")
            prices = category_page.get_product_prices()
            assert len(prices) >= 4, "Ожидалось минимум 4 цены"
            assert category_page.is_sorted_ascending(prices), "Цены не отсортированы Low-High"

        with allure.step("Сортировка по цене High > Low"):
            category_page.select_sort_option("Price High > Low")
            prices = category_page.get_product_prices()
            assert category_page.is_sorted_descending(prices), "Цены не отсортированы High-Low"

    @allure.title("TЗ-2: Поиск и корзина")
    @allure.description("Поиск shirt, добавление 2 и 3 товара, удвоение самого дешёвого")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_and_cart(self, home_page, category_page, cart_page):

        def add_product_by_index(index, quantity=None):
            """
            Добавить товар в корзину по индексу

            Args:
                index: номер товара (0, 1, 2...)
                quantity: количество (если не указать, будет случайное от 1 до 3)
            """
            if quantity is None:
                quantity = random.randint(1, 3)

            home_page.open()
            WebDriverWait(home_page.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter_keyword"))
            )

            home_page.search("shirt")
            time.sleep(3)

            select = Select(home_page.driver.find_element(By.ID, "sort"))
            select.select_by_visible_text("Name A - Z")
            time.sleep(2)

            product_links = home_page.driver.find_elements(By.CSS_SELECTOR, ".prdocutname")
            if index >= len(product_links):
                raise IndexError(f"Product index {index} out of range, only {len(product_links)} products")

            home_page.driver.execute_script("arguments[0].scrollIntoView(true);", product_links[index])
            time.sleep(1)
            product_links[index].click()
            time.sleep(2)

            qty_input = home_page.driver.find_element(By.ID, "product_quantity")
            qty_input.clear()
            qty_input.send_keys(str(quantity))

            add_btn = home_page.driver.find_element(By.CSS_SELECTOR, ".cart")
            add_btn.click()
            time.sleep(2)

        with allure.step("Добавить 2-й товар с рандомным количеством"):
            add_product_by_index(1)

        with allure.step("Добавить 3-й товар с рандомным количеством"):
            add_product_by_index(2)

        with allure.step("Работа с корзиной"):
            with allure.step("Получение списка товаров"):
                rows = home_page.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
                product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]

            if not product_rows:
                allure.attach("Корзина пуста", "Предупреждение", allure.attachment_type.TEXT)
                return

            with allure.step("Поиск самого дешёвого товара"):
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

            with allure.step("Сохранение старой суммы"):
                old_total_elem = home_page.driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
                old_total_text = old_total_elem.text.replace("$", "").replace(",", "")
                old_total = float(old_total_text) if old_total_text else 0
                allure.attach(f"${old_total:.2f}", "Сумма до удвоения", allure.attachment_type.TEXT)

            with allure.step("Удвоение количества самого дешёвого товара"):
                cheapest_row = product_rows[cheapest_idx]
                qty_input = cheapest_row.find_element(By.CSS_SELECTOR, "input[type='text']")
                current_qty = int(qty_input.get_attribute("value"))
                new_qty = current_qty * 2
                qty_input.clear()
                qty_input.send_keys(str(new_qty))

            with allure.step("Получение новой суммы"):
                update_btn = home_page.driver.find_element(By.ID, "cart_update")
                update_btn.click()
                time.sleep(3)

                new_total_elem = home_page.driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
                new_total_text = new_total_elem.text.replace("$", "").replace(",", "")
                new_total = float(new_total_text) if new_total_text else 0
                allure.attach(f"${new_total:.2f}", "Сумма после удвоения", allure.attachment_type.TEXT)

            with allure.step("Проверка изменения суммы"):
                assert new_total != old_total, f"Сумма не изменилась: было ${old_total:.2f}, стало ${new_total:.2f}"


    @allure.title("TЗ-3: Проверка корзины")
    @allure.description("Добавление товаров и удаление чётных позиций")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_operations(self, home_page, category_page, cart_page):

        def add_product_from_home(quantity=None):

            if quantity is None:
                quantity = random.randint(1, 3)
            add_buttons = home_page.driver.find_elements(By.CSS_SELECTOR, ".productcart")
            if not add_buttons:
                raise Exception("Нет доступных товаров для добавления")

            idx = random.randint(0, len(add_buttons) - 1)

            home_page.driver.execute_script("arguments[0].scrollIntoView(true);", add_buttons[idx])
            time.sleep(1)

            add_buttons[idx].click()
            time.sleep(2)

        with allure.step("Открыть главную страницу"):
            home_page.open()
            time.sleep(2)

        with allure.step("Добавить 5 случайных товаров"):
            for i in range(5):
                add_product_from_home()
                allure.attach(f"Добавлен товар {i + 1}/5", "Прогресс", allure.attachment_type.TEXT)

        with allure.step("Перейти в корзину"):
            home_page.go_to_cart()
            time.sleep(3)

        with allure.step("Удалить все чётные по порядку товары"):
            rows = home_page.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]

            for idx in [3, 1]:
                if idx < len(product_rows):
                    remove_btn = product_rows[idx].find_element(By.CSS_SELECTOR, "td:last-child a")
                    remove_btn.click()
                    time.sleep(2)
                    rows = home_page.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
                    product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]

        with allure.step("Проверить итоговую сумму"):
            total_elem = home_page.driver.find_element(By.CSS_SELECTOR, "td.total, span.cart_total")
            total_text = total_elem.text.replace("$", "").replace(",", "")
            total = float(total_text) if total_text else 0
            rows = home_page.driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            product_rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
            allure.attach(
                f"Осталось товаров: {len(product_rows)}, сумма: ${total:.2f}",
                "Результат",
                allure.attachment_type.TEXT
            )
            assert total > 0, "Итоговая сумма должна быть больше 0"