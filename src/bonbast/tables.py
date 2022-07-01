import math

from typing import List
from rich.table import Table
from rich.console import ConsoleRenderable

try:
    from .data import *
except:
    from data import *


def __get_currencies_sub_table(currencies: List[Currency]) -> ConsoleRenderable:
    table = Table()

    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Currency", style="cyan")
    table.add_column("Sell", style="green", no_wrap=True)
    table.add_column("Buy", style="green", no_wrap=True)

    for currency in currencies:
        table.add_row(
            currency.code,
            currency.name,
            currency.formatted_sell,
            currency.formatted_buy,
        )

    return table


def get_currencies_table(currencies: List[Currency], columns: int) -> ConsoleRenderable:
    """ Gets a list of data.Currency and generates currencies table
    """
    each_part_count = math.ceil(len(currencies) / columns)
    currencies_parts = [currencies[i:i + each_part_count] for i in range(0, len(currencies), each_part_count)]
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
    table.add_column("Sell", style="green", no_wrap=True)
    table.add_column("Buy", style="green", no_wrap=True)

    for coin in coins:
        table.add_row(
            coin.name,
            coin.formatted_sell,
            coin.formatted_buy,
        )

    return table


# get gold and it's price in a table
def get_gold_table(golds: List[Gold]) -> ConsoleRenderable:
    """ Gets a list of data.Gold and generates golds table
    """
    table = Table(title="Gold")

    table.add_column("Gold", style="cyan")
    table.add_column("Price", style="green", no_wrap=True)

    for gold in golds:
        table.add_row(
            gold.name,
            gold.formatted_price,
        )

    return table
