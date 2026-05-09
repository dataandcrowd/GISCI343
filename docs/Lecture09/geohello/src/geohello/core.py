"""Greeting function. The simplest unit of a package."""

from __future__ import annotations


def hello(place: str = "Auckland") -> str:
    """Return a greeting for a place.

    Parameters
    ----------
    place : str, default "Auckland"
        The place to greet.

    Returns
    -------
    str
        A greeting string.

    Examples
    --------
    >>> hello()
    'Hello from Auckland!'
    >>> hello("Tokyo")
    'Hello from Tokyo!'
    """
    return f"Hello from {place}!"
