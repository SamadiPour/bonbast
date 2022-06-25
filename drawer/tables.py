import math
from typing import List

from rich.console import ConsoleRenderable
from rich.table import Table

from drawer import Currency, Coin, Gold

PRICE_FORMATTER = "{:,}"


def build_currencies_table(currencies: List[Currency], columns: int) -> ConsoleRenderable:
    """
    Build a table of currencies and their prices.
    Parameters:
        currencies: List[Currency] - list of currencies to display
        columns: int - number of columns to display
    Returns:
        ConsoleRenderable - table of currencies and their prices
    """

    def build_currencies_sub_table(currencies_junk: List[Currency]) -> ConsoleRenderable:
        table = Table()

        table.add_column("Code", style="cyan", no_wrap=True)
        table.add_column("Currency", style="cyan")
        table.add_column("Buy", style="green", no_wrap=True)
        table.add_column("Sell", style="green", no_wrap=True)

        for currency in currencies_junk:
            table.add_row(
                currency.code,
                currency.name,
                PRICE_FORMATTER.format(currency.buy),
                PRICE_FORMATTER.format(currency.sell),
            )

        return table

    each_part_count = math.ceil(len(currencies) / columns)
    currencies_parts = [currencies[i:i + each_part_count] for i in range(0, len(currencies), each_part_count)]
    tables = [build_currencies_sub_table(junk) for junk in currencies_parts]

    grid = Table.grid(padding=5)
    grid.title = 'Currencies'
    for _ in range(columns):
        grid.add_column()
    grid.add_row(*tables)

    return grid


def build_coins_table(coins: List[Coin]) -> ConsoleRenderable:
    """
    Build a table of coins and their prices.
    Parameters:
        coins: List[Coin] - list of coins to display
    Returns:
        ConsoleRenderable - table of coins and their prices
    """
    table = Table(title="Coins")

    table.add_column("Coin", style="cyan")
    table.add_column("Buy", style="green", no_wrap=True)
    table.add_column("Sell", style="green", no_wrap=True)

    for coin in coins:
        table.add_row(
            coin.name,
            PRICE_FORMATTER.format(coin.buy),
            PRICE_FORMATTER.format(coin.sell),
        )

    return table


def build_gold_table(golds: List[Gold]) -> ConsoleRenderable:
    """
    Build a table of gold and its price.
    Parameters:
        golds: List[Gold] - list of gold to display
    Returns:
        ConsoleRenderable - table of gold and its price
    """
    table = Table(title="Gold")

    table.add_column("Gold", style="cyan")
    table.add_column("Price", style="green", no_wrap=True)

    for gold in golds:
        table.add_row(
            gold.name,
            PRICE_FORMATTER.format(gold.price),
        )

    return table


__all__ = [
    'build_currencies_table',
    'build_coins_table',
    'build_gold_table',
]
