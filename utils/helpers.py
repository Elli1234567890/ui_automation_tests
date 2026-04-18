import random
import allure


def attach_screenshot(driver, name="screenshot"):
    """Добавить скриншот в отчет Allure"""
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


def get_random_quantity(min_qty=1, max_qty=5):
    """Получить случайное количество"""
    return random.randint(min_qty, max_qty)