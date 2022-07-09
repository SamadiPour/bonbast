import datetime
from typing import Optional

try:
    from ..models.token import *
    from .storage_manager import *
    from ..helpers.utils import Singleton
    from ..server import get_token_from_main_page
except:  # noqa
    from src.bonbast.models.token import *
    from src.bonbast.managers.storage_manager import *
    from src.bonbast.helpers.utils import Singleton
    from src.bonbast.server import get_token_from_main_page


class TokenManager(object, metaclass=Singleton):
    _storage_manager = StorageManager(file_path=StorageManager.get_app_directory() / 'token.data')

    @staticmethod
    def _delete_token():
        TokenManager._storage_manager.delete_file()

    @staticmethod
    def _save_token(token: Token) -> None:
        TokenManager._storage_manager.save_file(f'{token.value}\n{token.generated_at.isoformat()}')

    @staticmethod
    def _load_token() -> Optional[Token]:
        try:
            token, date = TokenManager._storage_manager.load_file().splitlines()
            return Token(value=token, generated_at=datetime.datetime.fromisoformat(date))
        except FileNotFoundError:
            return None

    def generate(self):
        """
        :return: a new [fresh] Token instance
        """
        token = self._load_token()
        if token is None or token.is_expired():
            token = Token(get_token_from_main_page())
            self._save_token(token)

        return token

    def invalidate_token(self):
        self._delete_token()


token_manager = TokenManager()

__all__ = [
    'token_manager',
]
