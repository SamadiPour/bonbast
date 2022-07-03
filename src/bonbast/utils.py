import time

TOMAN_FORMATTER = "{:,}"
PRICE_FORMATTER = "{:,.2f}"


def format_toman(price: float) -> str:
    return TOMAN_FORMATTER.format(price)


def format_price(price: float) -> str:
    return PRICE_FORMATTER.format(price)


def retry(func, retry_count=3, retry_delay=None):
    def wrapper(*args, **kwargs):
        for _ in range(retry_count):
            try:
                return func(*args, **kwargs)
            except:  # noqa
                if retry_delay is not None:
                    time.sleep(retry_delay)

        raise Exception('Failed to get prices')

    return wrapper
