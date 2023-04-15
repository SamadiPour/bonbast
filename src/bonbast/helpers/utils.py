import time
import functools

TOMAN_FORMATTER = "{:,}"
PRICE_FORMATTER = "{:,.2f}"

DEFAULT_TEXT_COLOR = 'cyan'


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


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
