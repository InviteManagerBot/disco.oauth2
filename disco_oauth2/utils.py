from __future__ import annotations

from typing import (
    Any,
    Dict,
    Optional,
    Union,
    overload,
    Type,
    TypeVar,
    Any,
    TYPE_CHECKING,
)
from enum import Enum

import datetime
import json

try:
    import orjson
except ModuleNotFoundError:
    ORJSON = False
else:
    ORJSON = True

if TYPE_CHECKING:
    from aiohttp import ClientResponse

__all__ = ("_JSON_LOADER", "MISSING", "parse_time", "json_or_text")

E = TypeVar("E", bound="Enum")
T = TypeVar("T")

if ORJSON:

    def _to_json(obj: Any) -> str:
        return orjson.dumps(obj).decode("utf-8")  # type: ignore

    _JSON_LOADER = orjson.loads  # type: ignore
else:

    def _to_json(obj: Any) -> str:
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)

    _JSON_LOADER = json.loads


class _Missing:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _Missing()


@overload
def parse_time(timestamp: str) -> datetime.datetime:
    ...


@overload
def parse_time(timestamp: None) -> None:
    ...


def parse_time(timestamp: Optional[str]) -> Optional[datetime.datetime]:
    if not timestamp:
        return None
    return datetime.datetime.fromisoformat(timestamp)


@overload
def try_enum(cls: Type[E], value: None) -> None:
    ...


@overload
def try_enum(cls: Type[E], value: int) -> E:
    ...


def try_enum(cls: Type[E], value: Optional[int]) -> Optional[E]:
    try:
        return cls(value)
    except (ValueError, TypeError):
        return None


async def json_or_text(resp: ClientResponse) -> Union[Dict[str, Any], str]:
    text = await resp.text(encoding="utf-8")
    try:
        if resp.headers["content-type"] == "application/json":
            return _JSON_LOADER(text)
    except KeyError:
        pass

    return text


def copy_doc(target: Any):
    def decorator(overridden: Any):
        overridden.__doc__ = target.__doc__
        return overridden

    return decorator


# This is to avoid pyright raise a error when excpeted Snowflake and int received,
# this function will ensure that the Snowflake is a int, if available.
def get_snowflake(data: Any, key: str) -> Optional[int]:
    try:
        value = data[key]
    except KeyError:
        return None
    else:
        return value and int(value)
