import unittest
from src.bonbast.server import get_prices_from_api, get_token_from_main_page, get_graph_data, get_history

class TestServerFunctions(unittest.TestCase):
    def test_get_token_from_main_page(self):
        """Test that a token can be retrieved from the main page."""
        token = get_token_from_main_page()
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

    def test_get_prices_from_api(self):
        """Test that prices can be retrieved from the API."""
        token = get_token_from_main_page()
        currencies, coins, golds = get_prices_from_api(token)
        self.assertTrue(len(currencies) > 0)
        self.assertTrue(len(coins) > 0)
        self.assertTrue(len(golds) > 0)

    def test_get_graph_data(self):
        """Test that graph data can be retrieved."""
        data = get_graph_data('usd')
        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) > 0)

    def test_get_history(self):
        """Test that historical data can be retrieved."""
        from datetime import datetime, timedelta
        date = datetime.today() - timedelta(days=1)
        currencies, coins = get_history(date)
        self.assertTrue(len(currencies) > 0)
        self.assertTrue(len(coins) > 0)

if __name__ == '__main__':
    unittest.main()
