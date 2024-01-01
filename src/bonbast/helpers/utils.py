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
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def format_toman(price: float) -> str:
    return TOMAN_FORMATTER.format(price)


def format_price(price: float) -> str:
    return PRICE_FORMATTER.format(price)


class RetryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def retry(retry_count=3, retry_delay=None, message=''):
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
    if old_price is None or price is None:
        return ''

    if price > old_price:
        return 'green'
    elif price < old_price:
        return 'red'
    else:
        return ''


def get_change_char(price, old_price):
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
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience


def filter_valids(*items):
    return ([e for e in item if e.is_valid()] for item in items)


def print_json(*items, pretty=False, expanded=False):
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
    console = Console()
    for item in items:
        if item:
            console.print(item)
