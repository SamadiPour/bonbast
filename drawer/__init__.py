from typing import Tuple, List

from statics import *

BUY = '1'
SELL = '2'


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


def process_price_data(parsed_data: dict) -> Tuple[List[Currency], List[Coin], List[Gold]]:
    """
    Process the price data and return a list of currencies, coins and gold.
    Parameters:
        parsed_data: dict - parsed price data crawled from the API
    Returns:
        Tuple[List[Currency], List[Coin], List[Gold]] - list of currencies, coins and gold
    """
    currencies: List[Currency] = []
    coins: List[Coin] = []
    golds: List[Gold] = []

    for currency in CURRENCY_VALUES:
        if f'{currency}{BUY}' in parsed_data and f'{currency}{SELL}' in parsed_data:
            currencies.append(Currency(
                currency.upper(),
                CURRENCY_VALUES[currency],
                int(parsed_data[f'{currency}{BUY}']),
                int(parsed_data[f'{currency}{SELL}']),
            ))

    for coin in COIN_VALUES:
        if f'{coin}' in parsed_data and f'{coin}{SELL}' in parsed_data:
            coins.append(Coin(
                COIN_VALUES[coin],
                int(parsed_data[coin]),
                int(parsed_data[f'{coin}{SELL}']),
            ))

    for gold in GOLD_VALUES:
        if f'{gold}' in parsed_data:
            golds.append(Gold(
                GOLD_VALUES[gold],
                int(parsed_data[gold])
            ))

    return currencies, coins, golds


__all__ = [
    'Currency',
    'Coin',
    'Gold',
    'process_price_data',
]
