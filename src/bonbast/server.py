import re
from datetime import datetime, timedelta
from typing import Tuple, List, Optional, Dict

import requests
from bs4 import BeautifulSoup

try:
    from .models import *
except ImportError:
    from models import *

BASE_URL = 'https://www.bonbast.com'
USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/103.0.0.0 Mobile Safari/537.36'
SELL = '1'
BUY = '2'


def int_try_parse(value) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None


def get_token_from_main_page():
    """ This function gets a token from main page of bonbast.com
    This token should be saved somewhere because we are going to need it when we want to load pricest

    param dont_raise_error: It's on False by default. If you pass True it won't raise error because of connection problems.
        It will return False instead.
    """
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
        'user-agent': USER_AGENT,
    }

    try:
        r = requests.get(BASE_URL, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    search = re.search(r"param\s*=\s*\"(.+)\"", r.text, re.MULTILINE)
    if search is None or search.group(1) is None:
        raise SystemExit('Error: token not found in the main page')

    return search.group(1)


def get_prices_from_api(token: str) -> Tuple[List[Currency], List[Coin], List[Gold]]:
    """ Gets the prices' data from API using

    param token: You should pass the token that you got from get_token_from_main_page

    param dont_raise_error: It's on False by default. If you pass True it won't raise error because of connection problems.
        It will return False instead.
    """
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
        'user-agent': USER_AGENT,
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'data': token,
        'webdriver': 'false',
    }

    try:
        r = requests.post(f'{BASE_URL}/json', headers=headers, data=data)
        r.raise_for_status()
        r = r.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    if 'reset' in r:
        raise ResetAPIError('Error: token is expired')

    currencies: List[Currency] = []
    coins: List[Coin] = []
    golds: List[Gold] = []

    for currency in Currency.VALUES:
        if f'{currency}{BUY}' in r and f'{currency}{SELL}' in r:
            currencies.append(Currency(
                currency.upper(),
                Currency.VALUES[currency],
                sell=int(r[f'{currency}{SELL}']),
                buy=int(r[f'{currency}{BUY}']),
            ))

    for coin in Coin.VALUES:
        if f'{coin}' in r and f'{coin}{BUY}' in r:
            coins.append(Coin(
                coin,
                Coin.VALUES[coin],
                sell=int(r[coin]),
                buy=int(r[f'{coin}{BUY}']),
            ))

    for gold in Gold.VALUES:
        if f'{gold}' in r:
            golds.append(Gold(
                gold,
                Gold.VALUES[gold],
                price=int(r[gold])
            ))

    return currencies, coins, golds


def get_graph_data(
        currency: str,
        start_date: datetime = datetime.today() - timedelta(days=30),
        end_date: datetime = datetime.today(),
) -> Dict[str, int]:
    """
        This function will make a request to bonbast.com/graph and make them in two array.
    """

    headers = {
        'authority': 'bonbast.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'cookieconsent_status=true; st_bb=0',
        'referer': 'https://bonbast.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': USER_AGENT,
    }

    try:
        request = requests.get(f'{BASE_URL}/graph/{currency}/{start_date.date()}/{end_date.date()}', headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    soup = BeautifulSoup(request.text, 'html.parser')
    for data in soup.find_all("script"):
        # get variables from script and convert them to list
        if "data: {" in data.text:
            price_list = data.text.split("data: [")[1].split("]")[0].split(",")
            date_list = data.text.split("labels: [")[1].split("]")[0].split(',')

            if len(price_list) != len(date_list):
                raise SystemExit('Error: data inconsistency')

            dic = {}
            for i in range(len(price_list)):
                price = int(price_list[i])
                date = re.search(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', date_list[i]).group(0)
                dic[date] = price

            return dic


def get_history(date: datetime = datetime.today() - timedelta(days=1)) -> List[Currency]:
    if date.date() < datetime(2012, 10, 9).date():
        raise SystemExit('Error: date is too far in the past. Date must be greater than 2012-10-09')

    if date.date() >= datetime.today().date():
        raise SystemExit(f'Error: date must be less than today({date.today().date()}).')

    headers = {
        'authority': 'bonbast.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': USER_AGENT,
    }

    try:
        request = requests.get(f'{BASE_URL}/archive/{date.strftime("%Y/%m/%d")}', headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    soup = BeautifulSoup(request.text, 'html.parser')
    tables = soup.findAll("table")

    # first and second table are currencies
    currencies: List[Currency] = []
    for table in tables[0:1]:
        for row in table.findAll('tr')[1:]:
            cells = row.findAll("td")
            currencies.append(Currency(
                cells[0].text.lower(),
                Currency.VALUES[cells[0].text.lower()],
                sell=int_try_parse(cells[2].text),
                buy=int_try_parse(cells[3].text),
            ))

    # todo: parse it correctly
    # last table is coins
    # coins: List[Coin] = []
    # for table in tables[-1:]:
    #     for row in table.findAll('tr')[1:]:
    #         cells = row.findAll("td")
    #         coins.append(Coin(
    #             cells[0].text.lower(),
    #             Coin.VALUES[cells[0].text.lower()],
    #             sell=int_try_parse(cells[2].text),
    #             buy=int_try_parse(cells[3].text),
    #         ))

    return currencies


class ResetAPIError(Exception):
    """
    This exception is raised when the token is expired, and you have to get new one.
    """
    pass
