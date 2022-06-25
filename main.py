from rich.console import Console

from drawer import process_price_data
from drawer.tables import *
from parser import token_manager
from parser.price import get_prices_from_api


def get_prices():
    """
    Get prices from API
    """
    token = token_manager.valid_token
    response = get_prices_from_api(token.value)
    if 'reset' in response:
        # if we got a reset response, update the token
        token_manager.update_token()
        return get_prices()
    else:
        return response


if __name__ == '__main__':
    data = get_prices()
    currencies_list, coins_list, golds_list = process_price_data(data)

    currencies_table = build_currencies_table(currencies_list, 2)
    coins_table = build_coins_table(coins_list)
    gold_table = build_gold_table(golds_list)

    console = Console()
    console.print(currencies_table, coins_table, gold_table)
