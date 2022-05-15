__all__: list[str] = [
    "datetime_utcnow_aware",
    "get_modules",
    "parse_to_future_datetime",
    "parse_to_timedelta_from_now",
    "validate_and_encode_url",
]

import asyncio
import datetime
import functools
import pathlib
import re
import urllib.parse

from typing import Generator

import dateparser


def datetime_utcnow_aware() -> datetime.datetime:
    """Helper shorthand for returning now aware utc datetime

    Returns
    -------
    datetime.datetime
        The datetime now returned as utc aware
    """
    return datetime.datetime.now(datetime.timezone.utc)


def get_modules(
    path: str | pathlib.Path,
) -> Generator[pathlib.Path, None, None]:
    """Get the modules from a specified path

    Parameters
    ----------
    path : str | pathlib.Path
        The module to get the path of

    Returns
    -------
    typing.Generator[pathlib.Path, None, None]
        The paths of the modules
    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    return path.rglob("[!_]*.py")


async def parse_to_future_datetime(duration: str) -> datetime.datetime | None:
    """Parse string duration to datetime

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    duration_parsed : datetime.datetime
        The datetime from the input
    None
        If the duration is not parsable or is in the past
    """
    loop = asyncio.get_event_loop()
    duration_parsed = await loop.run_in_executor(
        None,
        functools.partial(
            dateparser.parse,
            date_string=duration,
            settings={  # type: ignore
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "STRICT_PARSING": True,
            },
        ),
    )

    if duration_parsed is None or duration_parsed < datetime_utcnow_aware():
        return None

    return duration_parsed


async def parse_to_timedelta_from_now(duration: str) -> datetime.timedelta | None:
    """Parse string duration to timedelta from now

    Parameters
    ----------
    duration : str
        The string to parse from

    Returns
    -------
    datetime.timedelta
        The timedelta from now rounded to the nearest second
    None
        If the duration is not parsable or is in the past
    """
    now = datetime_utcnow_aware()

    loop = asyncio.get_event_loop()
    duration_parsed = await loop.run_in_executor(
        None,
        functools.partial(
            dateparser.parse,
            date_string=duration,
            settings={  # type: ignore
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "STRICT_PARSING": True,
            },
        ),
    )

    if duration_parsed is None or duration_parsed < now:
        return None

    duration_seconds = round(duration_parsed.timestamp() - now.timestamp())
    return datetime.timedelta(seconds=duration_seconds)


def validate_and_encode_url(url: str) -> str | None:
    """Validate and encode a specifed url

    Parameters
    ----------
    url : str
        The url to validate and/or encode

    Returns
    -------
    str | None
        Returns the encoded url if valid, otherwise None
    """
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    url_match = re.match(url_regex, url)

    if url_match is None:
        return None

    return urllib.parse.quote_plus(url)
