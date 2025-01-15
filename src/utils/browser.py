import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from rotating_free_proxies import RotatingFreeProxies

def create_driver(headless=True, use_proxy=True):
    chrome_options = uc.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    
    if use_proxy:
        proxy_manager = RotatingFreeProxies()
        proxy = proxy_manager.get_working_proxy().get('https')
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    driver = uc.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None