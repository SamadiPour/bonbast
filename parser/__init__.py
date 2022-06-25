import datetime
import os
import re
import requests
from typing import Optional
from utilities import get_app_directory

BASE_URL = 'https://www.bonbast.com'
BASE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36' \
                  ' (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Token(object):
    def __init__(self, value=None, date=None):
        self._value = value if value is not None else self._get_token_from_main_page()
        self._date = date if type(date) is datetime.datetime else datetime.datetime.now()

    @property
    def value(self):
        return self._value

    @property
    def date(self):
        return self._date

    @value.setter
    def value(self, passed_value):
        self._value = passed_value

    @date.setter
    def date(self, passed_value):
        self._date = passed_value

    def update_values(self):
        self._value = self._get_token_from_main_page()
        self._date = datetime.datetime.now()

    def is_valid(self):
        """
        Check if the token is valid or not.
        A token will expire in 10 minutes.
        """
        return datetime.datetime.now() - self.date <= datetime.timedelta(minutes=9, seconds=45)

    @staticmethod
    def _get_token_from_main_page():
        """
        Get the token from the main page of bonbast.com
        """
        headers = {
            'authority': 'bonbast.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image'
                      '/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
            'user-agent': BASE_USER_AGENT
        }

        try:
            r = requests.get(BASE_URL, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        search = re.search(r"\$\.post\('/json',{\s*data:\"(.+)\"", r.text, re.MULTILINE)
        if search is None or search.group(1) is None:
            raise SystemExit('Error: token not found in the main page')

        return search.group(1)


class TokenManager(object, metaclass=Singleton):
    def __init__(self, token: Token):
        self._token = token
        self._save_token_to_disk()

    @property
    def valid_token(self):
        """
        Check if the token is valid or not and always return a valid token and also update the saved token in the disk.
        Params:
            None
        Returns:
            Token: A valid token object
        """
        if not self._token:
            if token := self._fetch_token_from_disk():
                self._token = token
            else:
                self._token = Token()
                return self._token

        if not self._token.is_valid():
            self.update_token()

        return self._token

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: Token):
        self._token = token
        self._save_token_to_disk()

    def update_token(self):
        """
        Update the token and save it to the disk.
        Params:
            None
        Returns:
            None
        """
        app_dir = get_app_directory()

        try:
            os.remove(app_dir / 'token.data')
        except FileNotFoundError:
            pass

        self._token.update_values()
        self._save_token_to_disk()

    def _save_token_to_disk(self):
        """
        Save the token to the disk.
        Params:
            None
        Returns:
            None
        """
        if not self._token:
            raise ValueError('The token is not set')

        app_dir = get_app_directory()
        app_dir.mkdir(parents=True, exist_ok=True)

        with open(app_dir / 'token.data', 'w') as file:
            file.write(f'{self.token.value}\n{self.token.date.isoformat()}')

    @staticmethod
    def _fetch_token_from_disk() -> Optional[Token]:
        """
        Fetch the token from the disk. If the token was not found in the disk, return None.
        Params:
            None
        Returns:
            Token: A token object or None
        """
        app_dir = get_app_directory()

        try:
            with open(app_dir / 'token.data', 'r') as f:
                token, date = f.read().splitlines()

        except FileNotFoundError:
            return None
        else:
            return Token(token, datetime.datetime.fromisoformat(date))


token_manager = TokenManager(token=Token())

__all__ = [
    'token_manager',
    'BASE_USER_AGENT',
    'BASE_URL',
    'requests'
]
