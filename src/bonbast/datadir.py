import sys
import pathlib

from datetime import datetime
from typing import Optional, Tuple, List


def get_datadir() -> pathlib.Path:
    """ Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


def get_app_directory() -> pathlib.Path:
    """ Returns a directory path
    where application data can be stored.
    """

    return get_datadir() / "bonbast"


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
