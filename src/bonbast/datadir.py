import sys
import pathlib
import os

from datetime import datetime
from typing import Optional, Tuple, List


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


def save_token(token: str, date: datetime) -> None:
    """ Gets token and expiration date for it and saves them in data directory
    """
    app_dir = get_app_directory()

    try:
        app_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass

    with open(app_dir / 'token.data', 'w') as f:
        f.write(f'{token}\n{date.isoformat()}')


def get_token() -> Tuple[Optional[str], Optional[datetime]]:
    """ Loads the saved token from datadir.

    Returns token, datetime
    Returns None, None if there is no saved token
    """
    app_dir = get_app_directory()

    try:
        with open(app_dir / 'token.data', 'r') as f:
            token, date = f.read().splitlines()
            return token, datetime.fromisoformat(date)
    except FileNotFoundError:
        return None, None


def delete_token():
    """ Delete the saved token from datadir
    """
    app_dir = get_app_directory()

    try:
        os.remove(app_dir / 'token.data')
    except FileNotFoundError:
        pass
