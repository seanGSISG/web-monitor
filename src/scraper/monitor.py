import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from tenacity import retry, stop_after_attempt, wait_fixed
from selenium.common.exceptions import ElementClickInterceptedException

from ..utils.logger import logger
from ..utils.browser import create_driver, wait_for_element
from ..config import BESTBUY_URL, BB_USERNAME, BB_PASSWORD

class BestBuyMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.proxy_failures = 0
        self.notifier = Notifier()

    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_fixed(RETRY_DELAY))
    def check_availability(self):
        try:
            response = self.session.get(BESTBUY_URL)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for "Add to Cart" button
            add_to_cart_btn = soup.find('button', {'class': 'add-to-cart-button'})
            return add_to_cart_btn is not None and 'disabled' not in str(add_to_cart_btn)
        except Exception as e:
            if "Proxy" in str(e):
                self.proxy_failures += 1
                if self.proxy_failures >= MAX_PROXY_FAILURES:
                    self.cleanup()
                    self.driver = create_driver(use_proxy=False)
            logger.error(f"Error checking availability: {str(e)}")
            raise

    def login(self):
        try:
            if not self.driver:
                self.driver = create_driver()
            
            self.driver.get("https://www.bestbuy.com/signin")
            
            # Wait for and fill in login form
            email_field = wait_for_element(self.driver, By.ID, "fld-e")
            password_field = wait_for_element(self.driver, By.ID, "fld-p1")
            
            email_field.send_keys(BB_USERNAME)
            password_field.send_keys(BB_PASSWORD)
            
            # Submit login form
            sign_in_btn = wait_for_element(self.driver, By.CSS_SELECTOR, "button[type='submit']")
            sign_in_btn.click()
            
            # Wait for login to complete
            sleep(5)
            return True
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def handle_captcha(self):
        try:
            captcha_iframe = wait_for_element(self.driver, By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']")
            if captcha_iframe:
                logger.warning("Captcha detected! Switching to non-proxy mode...")
                self.cleanup()
                self.driver = create_driver(use_proxy=False)
                return True
            return False
        except Exception:
            return False

    def purchase_item(self):
        try:
            if not self.driver:
                self.driver = create_driver()
            
            # Navigate to product page
            self.driver.get(BESTBUY_URL)
            
            # Click Add to Cart
            add_to_cart = wait_for_element(self.driver, By.CSS_SELECTOR, "button.add-to-cart-button")
            add_to_cart.click()
            
            # Go to cart
            self.driver.get("https://www.bestbuy.com/cart")
            
            # Click Checkout
            checkout_btn = wait_for_element(self.driver, By.CSS_SELECTOR, "button.checkout-button")
            checkout_btn.click()
            
            if self.handle_captcha():
                return self.purchase_item()  # Retry purchase after handling captcha
            
            # Wait for checkout page to load and complete purchase
            place_order_btn = wait_for_element(self.driver, By.CSS_SELECTOR, "button.place-order-button")
            place_order_btn.click()
            
            # Additional error handling for common checkout issues
            if wait_for_element(self.driver, By.CSS_SELECTOR, ".error-message"):
                raise Exception("Checkout error detected")
            
            self.notifier.notify("Successfully purchased RTX 5090!")
            logger.info("Purchase completed successfully!")
            return True
            
        except ElementClickInterceptedException:
            if self.handle_captcha():
                return self.purchase_item()
            return False
        except Exception as e:
            logger.error(f"Purchase failed: {str(e)}")
            return False

    def cleanup(self):
        if self.driver:
            self.driver.quit()