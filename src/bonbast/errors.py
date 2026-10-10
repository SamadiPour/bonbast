"""Exceptions raised by bonbast."""


class BonbastError(Exception):
    """Base class for every error bonbast raises."""


class NetworkError(BonbastError):
    """bonbast.com could not be reached or answered with an error."""


class ParseError(BonbastError):
    """bonbast.com answered with something bonbast could not understand.

    This usually means the website changed its layout.
    """


class InvalidDateError(BonbastError, ValueError):
    """A requested date is outside the range bonbast.com has data for."""
