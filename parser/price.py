from . import *


def get_prices_from_api(token):
    """
    Get prices from the API.
    Parameters:
        token: str - token to use for the request
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
        'user-agent': BASE_USER_AGENT,
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'data': token,
        'webdriver': 'false',
    }

    try:
        r = requests.post(f'{BASE_URL}/json', headers=headers, data=data)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return r.json()
