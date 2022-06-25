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

price_formatter = "{:,}"

base_url = 'https://www.bonbast.com'

CURRENCY_VALUES = {
    'usd': 'US Dollar',
    'eur': 'Euro',
    'gbp': 'British Pound',
    'chf': 'Swiss Franc',
    'cad': 'Canadian Dollar',
    'aud': 'Australian Dollar',
    'sek': 'Swedish Krona',
    'nok': 'Norwegian Krone',
    'rub': 'Russian Ruble',
    'thb': 'Thai Baht',
    'sgd': 'Singapore Dollar',
    'hkd': 'Hong Kong Dollar',
    'azn': 'Azerbaijani Manat',
    'amd': '10 Armenian Dram',
    'dkk': 'Danish Krone',
    'aed': 'UAE Dirham',
    'jpy': '10 Japanese Yen',
    'try': 'Turkish Lira',
    'cny': 'Chinese Yuan',
    'sar': 'Saudi Riyal',
    'inr': 'Indian Rupee',
    'myr': 'Malaysian Ringgit',
    'afn': 'Afghan Afghani',
    'kwd': 'Kuwaiti Dinar',
    'iqd': '100 Iraqi Dinar',
    'bhd': 'Bahraini Dinar',
    'omr': 'Omani Rial',
    'qar': 'Qatari Rial',
}

COIN_VALUES = {
    'emami1': 'Emami',
    'azadi1g': 'Gerami',
    'azadi1': 'Azadi',
    'azadi1_2': '½ Azadi',
    'azadi1_4': '¼ Azadi',
}

GOLD_VALUES = {
    'mithqal': 'Gold Mithqal',
    'gol18': 'Gold Gram',
}

buy = '1'
sell = '2'


class Currency:
    def __init__(self, code: str, name: str, buy: int, sell: int):
        self.code = code
        self.name = name
        self.buy = buy
        self.sell = sell


class Coin:
    def __init__(self, name: str, buy: int, sell: int):
        self.name = name
        self.buy = buy
        self.sell = sell


class Gold:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


# get the token from the main page of bonbast.com
def get_token_from_main_page():
    headers = {
        'authority': 'bonbast.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'no-cache',
        'cookie': 'cookieconsent_status=true; st_bb=0',
        'pragma': 'no-cache',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
    }

    try:
        r = requests.get(base_url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    search = re.search("\$\.post\('/json',{\s*data:\"(.+)\"", r.text, re.MULTILINE)
    if search is None or search.group(1) is None:
        raise SystemExit('Error: token not found in the main page')

    return search.group(1)


# get response by using token acquired from main page
def get_prices_from_api(token):
    headers = {
        'authority': 'bonbast.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'cookieconsent_status=true; st_bb=0',
        'origin': 'https://bonbast.com',
        'referer': 'https://bonbast.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'data': token,
        'webdriver': 'false',
    }

    try:
        r = requests.post(f'{base_url}/json', headers=headers, data=data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return r.json()


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def get_app_directory() -> pathlib.Path:
    """
    Returns a directory path
    where application data can be stored.
    """

    return get_datadir() / "bonbast"


# save token to use later
def save_token(token: str, date: datetime) -> None:
    app_dir = get_app_directory()

    try:
        app_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass

    with open(app_dir / 'token.data', 'w') as f:
        f.write(f'{token}\n{date.isoformat()}')


# retrieve token from storage
def get_token() -> Tuple[Optional[str], Optional[datetime]]:
    app_dir = get_app_directory()

    try:
        with open(app_dir / 'token.data', 'r') as f:
            token, date = f.read().splitlines()
            return token, datetime.fromisoformat(date)
    except FileNotFoundError:
        return None, None


# delete saved token
def delete_token():
    app_dir = get_app_directory()

    try:
        os.remove(app_dir / 'token.data')
    except FileNotFoundError:
        pass


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
            price_formatter.format(currency.buy),
            price_formatter.format(currency.sell),
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
            price_formatter.format(coin.buy),
            price_formatter.format(coin.sell),
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
            price_formatter.format(gold.price),
        )

    return table


def parse_price_data(data: dict) -> Tuple[List[Currency], List[Coin], List[Gold]]:
    currencies: List[Currency] = []
    coins: List[Coin] = []
    golds: List[Gold] = []

    for currency in CURRENCY_VALUES:
        if f'{currency}{buy}' in data and f'{currency}{sell}' in data:
            currencies.append(Currency(
                currency.upper(),
                CURRENCY_VALUES[currency],
                int(data[f'{currency}{buy}']),
                int(data[f'{currency}{sell}']),
            ))

    for coin in COIN_VALUES:
        if f'{coin}' in data and f'{coin}{sell}' in data:
            coins.append(Coin(
                COIN_VALUES[coin],
                int(data[coin]),
                int(data[f'{coin}{sell}']),
            ))

    for gold in GOLD_VALUES:
        if f'{gold}' in data:
            golds.append(Gold(
                GOLD_VALUES[gold],
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

