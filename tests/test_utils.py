import unittest
from src.bonbast.helpers.utils import format_price, get_color, get_change_char

class TestUtils(unittest.TestCase):

    def test_format_price(self):
        self.assertEqual(format_price(1000.0), "1,000.00")
        self.assertEqual(format_price(1000000.123), "1,000,000.12")

    def test_get_color(self):
        self.assertEqual(get_color(100, 90), 'green')
        self.assertEqual(get_color(80, 90), 'red')
        self.assertEqual(get_color(90, 90), '')

    def test_get_change_char(self):
        self.assertEqual(get_change_char(100, 90), '↑')
        self.assertEqual(get_change_char(80, 90), '↓')
        self.assertEqual(get_change_char(90, 90), '-')

if __name__ == '__main__':
    unittest.main()
