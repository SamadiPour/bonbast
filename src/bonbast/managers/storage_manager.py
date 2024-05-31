import os
import pathlib
import sys

try:
    from ..helpers.utils import Singleton
except:  # noqa
    from src.bonbast.helpers.utils import Singleton


class StorageManager(object, metaclass=Singleton):
    """
    Manages storage operations for the application, such as saving and loading files.

    Attributes:
        file_path (pathlib.Path): The path to the file being managed.
    """

    def __init__(self, file_path: pathlib.Path):
        """
        Initializes the StorageManager with a specific file path.

        Args:
            file_path (pathlib.Path): The path to the file to manage.
        """
        self.storage_path = StorageManager.get_app_directory()
        self.file_path = file_path

    @staticmethod
    def get_app_directory() -> pathlib.Path:
        """
        Determines the appropriate application data directory based on the operating system.
        - linux: ~/.local/share
        - macOS: ~/Library/Application Support
        - windows: C:/Users/<USER>/AppData/Roaming

        Returns:
            pathlib.Path: The path to the application data directory.
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
        """
        Saves content to a file at the specified file path.

        Args:
            content (str): The content to save to the file.
        """
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, 'w') as f:
            f.write(content)

    def load_file(self) -> str:
        """
        Loads content from a file at the specified file path.

        Returns:
            str: The content loaded from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        with open(self.file_path, 'r') as f:
            return f.read()

    def delete_file(self) -> None:
        """
        Deletes the file at the specified file path.
        """
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
