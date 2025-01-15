import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Best Buy Configuration
BESTBUY_URL = "https://www.bestbuy.com/site/nvidia-geforce-rtx-5090-32gb-gddr7-graphics-card-dark-gun-metal/6614151.p?skuId=6614151"
CHECK_INTERVAL = 30  # seconds

# Credentials
BB_USERNAME = os.getenv('BB_USERNAME')
BB_PASSWORD = os.getenv('BB_PASSWORD')

# Selenium Configuration
HEADLESS = True

# Notification Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Proxy Configuration
USE_PROXIES = True
MAX_PROXY_FAILURES = 3