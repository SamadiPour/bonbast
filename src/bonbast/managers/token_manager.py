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
    """
    Manages the generation and invalidation of API tokens.
    
    This class uses the Singleton design pattern to ensure that only one instance of the token manager exists.
    """
    _storage_manager = StorageManager(file_path=StorageManager.get_app_directory() / 'token.data')

    @staticmethod
    def _delete_token():
        """
        Deletes the current token from storage.
        """
        TokenManager._storage_manager.delete_file()

    @staticmethod
    def _save_token(token: Token) -> None:
        """
        Saves the given token to storage.

        Args:
            token (Token): The token to save.
        """
        TokenManager._storage_manager.save_file(f'{token.value}\n{token.generated_at.isoformat()}')

    @staticmethod
    def _load_token() -> Optional[Token]:
        """
        Loads the token from storage.

        Returns:
            Optional[Token]: The loaded token, or None if no token was found.
        """
        try:
            token, date = TokenManager._storage_manager.load_file().splitlines()
            return Token(value=token, generated_at=datetime.datetime.fromisoformat(date))
        except FileNotFoundError:
            return None

    def generate(self) -> Token:
        """
        Generates a new token, either by loading it from storage or by requesting a new one from the server.

        Returns:
            Token: The generated or loaded token.
        """
        token = self._load_token()
        if token is None or token.is_expired():
            token = Token(get_token_from_main_page())
            self._save_token(token)

        return token

    def invalidate_token(self):
        """
        Invalidates the current token, forcing a new token to be generated on the next request.
        """
        self._delete_token()


token_manager = TokenManager()

__all__ = [
    'token_manager',
]
