# UI Automation Tests for automationteststore.com

[![CI/CD](https://github.com/Elli1234567890/ui_automation_tests/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Elli1234567890/ui_automation_tests/actions/workflows/run_tests.yml)

## Описание

UI-автотесты для интернет-магазина [automationteststore.com](https://automationteststore.com/).

**Технологии:**
- Python 3.10
- Selenium WebDriver
- Pytest + pytest-xdist (параллельный запуск)
- Allure Reports
- GitHub Actions CI/CD
- Поддержка Chrome и Firefox

## Установка и запуск

```bash
# Клонирование
git clone https://github.com/Elli1234567890 /ui_automation_tests.git
cd ui_automation_tests

# Создание виртуального окружения
python3.10 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Параллельный запуск тестов (Chrome)
pytest -n 3 --browser=chrome

# Параллельный запуск тестов (Firefox)
pytest -n 3 --browser=firefox

# Запуск с Allure отчетом
pytest --alluredir=allure-results
allure serve allure-results
