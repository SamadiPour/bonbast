import os
import pathlib
import sys
from collections import namedtuple
from datetime import datetime

try:
    from .token import Token
    from ..utils import Singleton
except ImportError:
    from src.bonbast.managers.token import Token
    from src.bonbast.utils import Singleton


class StorageManager(object, metaclass=Singleton):
    def __init__(self):
        self.storage_path = StorageManager.get_app_directory()
        self.token_file_path = self.storage_path / 'token.data'

    @staticmethod
    def get_app_directory() -> pathlib.Path:
        """ Returns a directory path
        data directory is where persistent application data can be stored.
        - linux: ~/.local/share
        - macOS: ~/Library/Application Support
        - windows: C:/Users/<USER>/AppData/Roaming

        the final directory is where application data can be stored.
        """

        home = pathlib.Path.home()

        if sys.platform == "win32":
            data_dir = home / "AppData/Roaming"
        elif sys.platform == "linux":
            data_dir = home / ".local/share"
        elif sys.platform == "darwin":
            data_dir = home / "Library/Application Support"
        else:
            raise NotImplementedError(f"Platform {sys.platform} is not supported")

        return data_dir / "bonbast"

    def save_token(self, token_value, generated_date):
        """ Gets token it in data directory
        """
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with open(self.token_file_path, 'w') as f:
            f.write(f'{token_value}\n{generated_date.isoformat()}')

    def get_token(self):
        """ Loads the saved token from datadir.
        Returns token, datetime
        Raise FileNotFoundError if no token was founded
        """
        with open(self.token_file_path, 'r') as f:
            token, date = f.read().splitlines()
            return namedtuple('Token', 'value generated_at')(token, datetime.fromisoformat(date))

    def delete_token(self) -> None:
        """ Delete the saved token from datadir
        """
        try:
            os.remove(self.token_file_path)
        except FileNotFoundError:
            pass


storage_manager = StorageManager()

__all__ = [
    'storage_manager',
]
