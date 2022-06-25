from pathlib import Path
import sys


def get_data_directory() -> Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def get_app_directory() -> Path:
    """
    Returns a directory path
    where application data can be stored.
    """

    return get_data_directory() / "bonbast"
