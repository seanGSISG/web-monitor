from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import undetected_chromedriver as uc
from typing import Optional
import requests

from ..config import HEADLESS, USE_PROXIES, WAIT_TIMEOUT

def get_free_proxy() -> str:
    """Get a free proxy from a public proxy list."""
    try:
        response = requests.get('https://proxylist.geonode.com/api/proxy-list?filterUpTime=90&protocols=http%2Chttps&limit=1&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=60')
        data = response.json()
        if data['data']:
            proxy = data['data'][0]
            return f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
        return ''
    except Exception:
        return ''

def create_driver(headless: bool = HEADLESS, use_proxy: bool = USE_PROXIES) -> WebDriver:
    chrome_options = uc.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')

    if use_proxy:
        proxy = get_free_proxy()
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')

    driver = uc.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def wait_for_element(
        driver: WebDriver,
        by: By,
        value: str,
        timeout: int = WAIT_TIMEOUT) -> Optional[WebElement]:
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None
