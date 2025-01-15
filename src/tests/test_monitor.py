import unittest
from unittest.mock import patch, MagicMock
from ..scraper.monitor import BestBuyMonitor


class TestBestBuyMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = BestBuyMonitor()

    def test_check_availability_success(self):
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.content = """
                <button class="add-to-cart-button">Add to Cart</button>
            """
            self.assertTrue(self.monitor.check_availability())

    def test_check_availability_not_available(self):
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.content = """
                <button class="add-to-cart-button" disabled>Sold Out</button>
            """
            self.assertFalse(self.monitor.check_availability())

    def tearDown(self):
        self.monitor.cleanup()


if __name__ == '__main__':
    unittest.main()
