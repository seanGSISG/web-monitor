import unittest
from unittest.mock import patch
from ..scraper.monitor import BestBuyMonitor
from ..utils.logger import logger

class TestBestBuyMonitor(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test case")
        self.monitor = BestBuyMonitor()

    def test_check_availability_success(self):
        logger.info("Testing product availability - success case")
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.content = """
                <button class="add-to-cart-button">Add to Cart</button>
            """
            self.assertTrue(self.monitor.check_availability())
            logger.info("Product availability test passed")

    def test_check_availability_not_available(self):
        logger.info("Testing product availability - not available case")
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.content = """
                <button class="add-to-cart-button" disabled>Sold Out</button>
            """
            self.assertFalse(self.monitor.check_availability())
            logger.info("Product not available test passed")

    def tearDown(self):
        logger.info("Cleaning up test case")
        self.monitor.cleanup()

if __name__ == '__main__':
    unittest.main()
