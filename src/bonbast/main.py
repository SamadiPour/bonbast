import math
import os
import pathlib
import re
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple, List

import requests
from rich.console import Console, ConsoleRenderable
from rich.table import Table

try:
    from .server import get_token_from_main_page, get_prices_from_api
    from .datadir import save_token, get_token, delete_token
    from .data import Currency, Coin, Gold
except:
    from server import get_token_from_main_page, get_prices_from_api
    from datadir import save_token, get_token, delete_token
    from data import Currency, Coin, Gold


PRICE_FORMATTER = "{:,}"


BUY = '1'
SELL = '2'


def get_prices():
    # get token from storage
    # check if token's time and make sure it's not expired
    token, token_date = get_token()
    if token is not None:
        # token will expire in 10 minutes
        # if expired, delete it and get a new one
        if datetime.now() - token_date > timedelta(minutes=9, seconds=45):
            delete_token()
            return get_prices()
    else:
        # if we don't have a token, we will get it from the main page
        token = get_token_from_main_page()
        save_token(token, datetime.now())

    # get prices from the api with the token acquired from main page
    response = get_prices_from_api(token)
    if 'reset' in response:
        # if we got a reset response, delete the token and get a new one
        delete_token()
        return get_prices()
    else:
        return response


def __get_currencies_sub_table(currencies: List[Currency]) -> ConsoleRenderable:
    table = Table()

    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Currency", style="cyan")
    table.add_column("Buy", style="green", no_wrap=True)
    table.add_column("Sell", style="green", no_wrap=True)

    for currency in currencies:
        table.add_row(
            currency.code,
            currency.name,
            PRICE_FORMATTER.format(currency.buy),
            PRICE_FORMATTER.format(currency.sell),
        )

    return table


# get currencies and prices in a table
def get_currencies_table(currencies: List[Currency], columns: int) -> ConsoleRenderable:
    each_part_count = math.ceil(len(currencies) / columns)
    currencies_parts = [currencies[i:i + each_part_count] for i in range(0, len(currencies), each_part_count)]
    tables = [__get_currencies_sub_table(part) for part in currencies_parts]

    grid = Table.grid(padding=5)
    grid.title = 'Currencies'
    for _ in range(columns):
        grid.add_column()
    grid.add_row(*tables)

    return grid


# get coins and prices in a table
def get_coins_table(coins: List[Coin]) -> ConsoleRenderable:
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


# get gold and it's price in a table
def get_gold_table(golds: List[Gold]) -> ConsoleRenderable:
    table = Table(title="Gold")

    table.add_column("Gold", style="cyan")
    table.add_column("Price", style="green", no_wrap=True)

    for gold in golds:
        table.add_row(
            gold.name,
            PRICE_FORMATTER.format(gold.price),
        )

    return table


def parse_price_data(data: dict) -> Tuple[List[Currency], List[Coin], List[Gold]]:
    currencies: List[Currency] = []
    coins: List[Coin] = []
    golds: List[Gold] = []

    for currency in Currency.CURRENCY_VALUES:
        if f'{currency}{BUY}' in data and f'{currency}{SELL}' in data:
            currencies.append(Currency(
                currency.upper(),
                Currency.CURRENCY_VALUES[currency],
                int(data[f'{currency}{BUY}']),
                int(data[f'{currency}{SELL}']),
            ))

    for coin in Coin.COIN_VALUES:
        if f'{coin}' in data and f'{coin}{sell}' in data:
            coins.append(Coin(
                Coin.COIN_VALUES[coin],
                int(data[coin]),
                int(data[f'{coin}{sell}']),
            ))

    for gold in Gold.GOLD_VALUES:
        if f'{gold}' in data:
            golds.append(Gold(
                Gold.GOLD_VALUES[gold],
                int(data[gold])
            ))

    return currencies, coins, golds


def cli_main():
    data = get_prices()
    currencies_list, coins_list, golds_list = parse_price_data(data)

    currencies_table = get_currencies_table(currencies_list, 2)
    coins_table = get_coins_table(coins_list)
    gold_table = get_gold_table(golds_list)

    console = Console()
    console.print(currencies_table, coins_table, gold_table)


if __name__ == '__main__':
    cli_main()

