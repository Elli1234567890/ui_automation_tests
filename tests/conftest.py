import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox",
                     help="Browser: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser in headless mode")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser == "firefox":
        options = Options()
        if headless:
            options.add_argument("--headless")
        service = Service("/usr/bin/geckodriver")
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from webdriver_manager.chrome import ChromeDriverManager
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    return "https://automationteststore.com/"
