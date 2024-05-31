import functools
import json
import time

import click
from rich.console import Console
from rich.pretty import pprint

TOMAN_FORMATTER = "{:,}"
PRICE_FORMATTER = "{:,.2f}"

DEFAULT_TEXT_COLOR = 'cyan'


class Singleton(type):
    """
    A metaclass for implementing the Singleton design pattern.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def format_toman(price: float) -> str:
    """
    Formats a price as a string in Toman currency format.

    :param price: The price to format.
    :return: The formatted price string.
    """
    return TOMAN_FORMATTER.format(price)


def format_price(price: float) -> str:
    """
    Formats a price as a string with two decimal places.

    :param price: The price to format.
    :return: The formatted price string.
    """
    return PRICE_FORMATTER.format(price)


class RetryError(Exception):
    """
    Custom exception class for retry failures.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def retry(retry_count=3, retry_delay=None, message=''):
    """
    A decorator for retrying a function call with a specified number of attempts and delay.

    :param retry_count: Number of retry attempts.
    :param retry_delay: Delay between retries.
    :param message: Message to display on failure.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            for i in range(retry_count):
                try:
                    return func(*args, **kwargs)
                except RetryError as e:
                    if i == retry_count - 1:
                        raise SystemExit(e.message)
                except Exception as e:  # noqa
                    if retry_delay is not None:
                        time.sleep(retry_delay)

            raise SystemExit(message)

        return wrapper_retry

    return decorator_retry


def get_color(price, old_price):
    """
    Determines the color based on the comparison of the current and old price.

    :param price: The current price.
    :param old_price: The old price.
    :return: The color string.
    """
    if old_price is None or price is None:
        return ''

    if price > old_price:
        return 'green'
    elif price < old_price:
        return 'red'
    else:
        return ''


def get_change_char(price, old_price):
    """
    Determines the change character based on the comparison of the current and old price.

    :param price: The current price.
    :param old_price: The old price.
    :return: The change character string.
    """
    if old_price is None or price is None:
        return ''

    if price > old_price:
        return '↑'
    elif price < old_price:
        return '↓'
    else:
        return '-'


def del_none(d):
    """
    Deletes keys with the value `None` in a dictionary, recursively.

    :param d: The dictionary to process.
    :return: The processed dictionary.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


def filter_valids(*items):
    """
    Filters out invalid items from a list of items based on their `is_valid` method.

    :param items: The items to filter.
    :return: A generator of filtered items.
    """
    return ([e for e in item if e.is_valid()] for item in items)


def print_json(*items, pretty=False, expanded=False):
    """
    Prints items as JSON, with options for pretty printing and expansion.

    :param items: The items to print.
    :param pretty: Whether to pretty print.
    :param expanded: Whether to expand all fields.
    """
    prices = {}
    for item in items:
        for model in item:
            prices.update(model.to_json())

    prices = del_none(prices)

    if pretty:
        pprint(prices, expand_all=expanded)
    else:
        click.echo(json.dumps(prices, ensure_ascii=False))


def print_tables(*items):
    """
    Prints items as tables using the Rich library.

    :param items: The items to print.
    """
    console = Console()
    for item in items:
        if item:
            console.print(item)
