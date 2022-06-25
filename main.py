import os
import pathlib
import re
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple

import requests as requests
from rich.console import Console
from rich.table import Table

price_formatter = "{:,}"

base_url = 'https://www.bonbast.com'

currencies = {
    'try': 'Turkish Lira',
    'afn': 'Afghan Afghani',
    'bhd': 'Bahraini Dinar',
    'cny': 'Chinese Yuan',
    'cad': 'Canadian Dollar',
    'usd': 'United States Dollar',
    'thb': 'Thai Baht',
    'azn': 'Azerbaijani Manat',
    'amd': '10 Armenian Dram',
    'rub': 'Russian Ruble',
    'eur': 'Euro',
    'chf': 'Swiss Franc',
    'jpy': '10 Japanese Yen',
    'kwd': 'Kuwaiti Dinar',
    'gbp': 'British Pound',
    'sek': 'Swedish Krona',
    'myr': 'Malaysian Ringgit',
    'omr': 'Omani Rial',
    'aud': 'Australian Dollar',
    'dkk': 'Danish Krone',
    'inr': 'Indian Rupee',
    'aed': 'UAE Dirham',
    'qar': 'Qatari Rial',
    'iqd': '100 Iraqi Dinar',
    'hkd': 'Hong Kong Dollar',
    'sar': 'Saudi Riyal',
    'sgd': 'Singapore Dollar',
    'nok': 'Norwegian Krone',
}

coins = {
    'emami1': 'Emami',
    'azadi1g': 'Gerami',
    'azadi1': 'Azadi',
    'azadi1_2': '½ Azadi',
    'azadi1_4': '¼ Azadi',
}

golds = {
    'mithqal': 'Gold Mithqal',
    'gol18': 'Gold Gram',
}

buy = '1'
sell = '2'


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


# get currencies and prices in a table
def get_currencies_table(data: dict) -> Table:
    table = Table(title="Currencies")

    table.add_column("Code", style="cyan", no_wrap=True)
    table.add_column("Currency", style="cyan")
    table.add_column("Buy", style="green", no_wrap=True)
    table.add_column("Sell", style="green", no_wrap=True)

    for currency in currencies:
        if f'{currency}{buy}' in data and f'{currency}{sell}' in data:
            table.add_row(
                currency.upper(),
                currencies[currency],
                price_formatter.format(int(data[f'{currency}{buy}'])),
                price_formatter.format(int(data[f'{currency}{sell}'])),
            )

    return table


# get coins and prices in a table
def get_coins_table(data: dict) -> Table:
    table = Table(title="Coins")

    table.add_column("Coin", style="cyan")
    table.add_column("Buy", style="green", no_wrap=True)
    table.add_column("Sell", style="green", no_wrap=True)

    for coin in coins:
        if f'{coin}' in data and f'{coin}{sell}' in data:
            table.add_row(
                coins[coin],
                price_formatter.format(int(data[f'{coin}'])),
                price_formatter.format(int(data[f'{coin}{sell}'])),
            )

    return table


# get gold and it's price in a table
def get_gold_table(data: dict) -> Table:
    table = Table(title="Gold")

    table.add_column("Gold", style="cyan")
    table.add_column("Price", style="green", no_wrap=True)

    for gold in golds:
        if f'{gold}' in data:
            table.add_row(
                golds[gold],
                price_formatter.format(int(data[f'{gold}'])),
            )

    return table


if __name__ == '__main__':
    data = get_prices()

    currencies_table = get_currencies_table(data)
    coins_table = get_coins_table(data)
    gold_table = get_gold_table(data)

    console = Console()
    console.print(currencies_table, coins_table, gold_table)
