import sys
import pathlib
import os

from datetime import datetime
from typing import Optional, Tuple, List


# needs to be singleton
class StorageManager(object):
    _instance = None

    def __init__(self):
        self.storage_path = StorageManager.get_app_directory()
        self.token_file_path = self.storage_path / 'token.data'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StorageManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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

    def save_token(self, token: str, date: datetime) -> None:
        """ Gets token and expiration date for it and saves them in data directory
        """
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass

        with open(self.token_file_path, 'w') as f:
            f.write(f'{token}\n{date.isoformat()}')

    def get_token(self) -> Tuple[Optional[str], Optional[datetime]]:
        """ Loads the saved token from datadir.

        Returns token, datetime
        Returns None, None if there is no saved token
        """
        try:
            with open(self.token_file_path, 'r') as f:
                token, date = f.read().splitlines()
                return token, datetime.fromisoformat(date)
        except FileNotFoundError:
            return None, None

    def delete_token(self) -> None:
        """ Delete the saved token from datadir
        """
        try:
            os.remove(self.token_file_path)
        except FileNotFoundError:
            pass
