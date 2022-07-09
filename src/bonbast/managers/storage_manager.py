import os
import pathlib
import sys

try:
    from ..helpers.utils import Singleton
except:  # noqa
    from src.bonbast.helpers.utils import Singleton


class StorageManager(object):
    def __init__(self, file_path: pathlib.Path):
        self.storage_path = StorageManager.get_app_directory()
        self.file_path = file_path

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

    def save_file(self, content: str) -> None:
        """ Gets token it in data directory
        """
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, 'w') as f:
            f.write(content)

    def load_file(self) -> str:
        """ Loads the saved token from datadir.
        Returns token, datetime
        Raise FileNotFoundError if no token was founded
        """
        with open(self.file_path, 'r') as f:
            return f.read()

    def delete_file(self) -> None:
        """ Delete the saved token from datadir
        """
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
