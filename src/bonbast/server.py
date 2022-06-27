import requests
import re


BASE_URL = 'https://www.bonbast.com'


HEADERS = {
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
""" These headers will be sent in each request that we make to bonbast.com
It makes bonbast.com think that we are a browser, so it won't block the IP address
"""


def get_token_from_main_page(dont_raise_error=False):
    """ This function gets a token from main page of bonbast.com
    This token should be saved somewhere because we are going to need it when we want to load pricest

    param dont_raise_error: It's on False by default. If you pass True it won't raise error because of connection problems.
        It will return False instead.
    """
    try:
        r = requests.get(BASE_URL, headers=HEADERS)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if dont_raise_error:
            return False
        raise SystemExit(err)

    search = re.search("\$\.post\('/json',{\s*data:\"(.+)\"", r.text, re.MULTILINE)
    if search is None or search.group(1) is None:
        if dont_raise_error:
            return False
        raise SystemExit('Error: token not found in the main page')

    return search.group(1)


def get_prices_from_api(token, dont_raise_error=False):
    """ Gets the prices data from API using

    param token: You should pass the token that you got from get_token_from_main_page

    param dont_raise_error: It's on False by default. If you pass True it won't raise error because of connection problems.
        It will return False instead.
    """
    data = {
        'data': token,
        'webdriver': 'false',
    }

    try:
        r = requests.post(f'{BASE_URL}/json', headers=HEADERS, data=data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if dont_raise_error:
            return False
        raise SystemExit(err)

    return r.json()
