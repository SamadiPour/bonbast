import argparse
from datetime import datetime, timedelta
from typing import Tuple, List

from rich.console import Console

try:
    from .server import get_token_from_main_page, get_prices_from_api
    from .storage_manager import StorageManager
    from .data import Currency, Coin, Gold
    from .tables import get_currencies_table, get_coins_table, get_gold_table
except:
    from server import get_token_from_main_page, get_prices_from_api
    from storage_manager import StorageManager
    from data import Currency, Coin, Gold
    from tables import get_currencies_table, get_coins_table, get_gold_table


BUY = '1'
SELL = '2'


def get_prices():
    # get token from storage
    # check if token's time and make sure it's not expired
    token, token_date = StorageManager().get_token()
    if token is not None:
        # token will expire in 10 minutes
        # if expired, delete it and get a new one
        if datetime.now() - token_date > timedelta(minutes=9, seconds=45):
            StorageManager().delete_token()
            return get_prices()
    else:
        # if we don't have a token, we will get it from the main page
        token = get_token_from_main_page()
        StorageManager().save_token(token, datetime.now())

    # get prices from the api with the token acquired from main page
    response = get_prices_from_api(token)
    if 'reset' in response:
        # if we got a reset response, delete the token and get a new one
        StorageManager().delete_token()
        return get_prices()
    else:
        return response


def parse_price_data(data: dict) -> Tuple[List[Currency], List[Coin], List[Gold]]:
    currencies: List[Currency] = []
    coins: List[Coin] = []
    golds: List[Gold] = []

    for currency in Currency.VALUES:
        if f'{currency}{BUY}' in data and f'{currency}{SELL}' in data:
            currencies.append(Currency(
                currency.upper(),
                Currency.VALUES[currency],
                int(data[f'{currency}{BUY}']),
                int(data[f'{currency}{SELL}']),
            ))

    for coin in Coin.VALUES:
        if f'{coin}' in data and f'{coin}{SELL}' in data:
            coins.append(Coin(
                coin,
                Coin.VALUES[coin],
                int(data[coin]),
                int(data[f'{coin}{SELL}']),
            ))

    for gold in Gold.VALUES:
        if f'{gold}' in data:
            golds.append(Gold(
                gold,
                Gold.VALUES[gold],
                int(data[gold])
            ))

    return currencies, coins, golds


def cli_main():
    parser = argparse.ArgumentParser(description='See bonbast.com prices in your command line!')

    parser.add_argument('--only-currencies', dest='only_currencies', action="store_true",
        help='Only show currencies table')
    parser.add_argument('--only-coins', dest='only_coins', action="store_true",
        help='Only show coins table')
    parser.add_argument('--only-golds', dest='only_golds', action="store_true",
        help='Only show golds table')
    parser.add_argument('--json', dest='json', action="store_true",
        help='Print json output received from server')

    args = parser.parse_args()

    data = get_prices()
    if args.json:
        print(data)
        return

    currencies_list, coins_list, golds_list = parse_price_data(data)

    console = Console()

    # if none of these flags are sent, show all of tables
    show_all_tables = not args.only_currencies and not args.only_coins and not args.only_golds

    if show_all_tables or args.only_currencies:
        currencies_table = get_currencies_table(currencies_list, 2)
        console.print(currencies_table)

    if show_all_tables or args.only_coins:
        coins_table = get_coins_table(coins_list)
        console.print(coins_table)

    if show_all_tables or args.only_golds:
        gold_table = get_gold_table(golds_list)
        console.print(gold_table)


if __name__ == '__main__':
    cli_main()

