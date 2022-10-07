import math

from typing import List
from rich.table import Table
from rich.console import ConsoleRenderable

try:
    from .models import *
except ImportError:
    from models import *


def __get_currencies_sub_table(currencies: List[Currency]) -> ConsoleRenderable:
    table = Table()

    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Currency", style="cyan")
    table.add_column("Sell", no_wrap=True)
    table.add_column("Buy", no_wrap=True)

    for currency in currencies:
        table.add_row(
            currency.code,
            currency.name,
            currency.formatted_sell if currency.sell is not None else '-',
            currency.formatted_buy if currency.buy is not None else '-',
        )

    return table


def get_currencies_table(currencies: List[Currency], columns: int) -> ConsoleRenderable:
    """ Gets a list of data.Currency and generates currencies table
    """

    filtered_currencies = [
        currency for currency in currencies if
        (currency.sell is not None or currency.buy is not None) and (currency.sell != 0 or currency.buy != 0)
    ]

    if len(filtered_currencies) < 6:
        columns = 1

    each_part_count = math.ceil(len(filtered_currencies) / columns)
    currencies_parts = [
        filtered_currencies[i:i + each_part_count] for i in
        range(0, len(filtered_currencies), each_part_count)
    ]
    tables = [__get_currencies_sub_table(part) for part in currencies_parts]

    grid = Table.grid(padding=5)
    grid.title = 'Currencies'
    for _ in range(columns):
        grid.add_column()
    grid.add_row(*tables)

    return grid


def get_coins_table(coins: List[Coin]) -> ConsoleRenderable:
    """ Gets a list of data.Coin and generates coins table
    """
    table = Table(title="Coins")

    table.add_column("Coin", style="cyan")
    table.add_column("Sell", no_wrap=True)
    table.add_column("Buy", no_wrap=True)

    for coin in coins:
        table.add_row(
            coin.name,
            coin.formatted_sell if coin.sell is not None else '-',
            coin.formatted_buy if coin.buy is not None else '-',
        )

    return table


# get gold and it's price in a table
def get_gold_table(golds: List[Gold]) -> ConsoleRenderable:
    """ Gets a list of data.Gold and generates golds table
    """
    table = Table(title="Gold")

    table.add_column("Gold", style="cyan")
    table.add_column("Price", no_wrap=True)

    for gold in golds:
        table.add_row(
            gold.name,
            gold.formatted_price if gold.price is not None else '-',
        )

    return table
