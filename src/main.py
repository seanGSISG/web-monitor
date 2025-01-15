import time
from typing import NoReturn

from scraper.monitor import BestBuyMonitor
from utils.logger import logger
from config import CHECK_INTERVAL


def main() -> NoReturn:
    monitor = BestBuyMonitor()
    consecutive_errors = 0
    logger.info("Starting Best Buy RTX 5090 Monitor")
    
    try:
        while True:
            try:
                if not monitor.driver:
                    if not monitor.login():
                        logger.error("Failed to login. "
                                   "Retrying in 30 seconds...")
                        time.sleep(30)
                        continue

                if monitor.check_availability():
                    logger.info(
                        "RTX 5090 is available! Attempting to purchase...")
                    monitor.notifier.notify(
                        "RTX 5090 found! Attempting purchase...")
                    if monitor.purchase_item():
                        break
                    else:
                        consecutive_errors += 1
                else:
                    consecutive_errors = 0
                    logger.info("RTX 5090 is not available. Waiting for next check...")

                if consecutive_errors >= 3:
                    logger.warning("Too many consecutive errors. Restarting session...")
                    monitor.cleanup()
                    monitor.driver = None
                    consecutive_errors = 0

                time.sleep(CHECK_INTERVAL)

            except Exception as e:
                logger.error(f"An error occurred: {str(e)}")
                consecutive_errors += 1
                time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main()