TOMAN_FORMATTER = "{:,}"
PRICE_FORMATTER = "{:,.2f}"


def format_toman(price: float) -> str:
    return TOMAN_FORMATTER.format(price)


def format_price(price: float) -> str:
    return PRICE_FORMATTER.format(price)
