from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union, Dict

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    Response = ClientResponse

__all__ = (
    "Oauth2Exception",
    "HTTPException",
    "Forbidden",
    "NotFound",
    "DiscordServerError",
)


class Oauth2Exception(Exception):
    """Base exception class for discord-oauth2"""

    pass


class HTTPException(Oauth2Exception):
    """Exception that's raised when HTTP request fails.

    Attributes
    ---------
    response: Union[:class:`requests.Response`, :class:`aiohttp.ClientResponse`]
        The response object of the failed HTTP request.
        This will be an :class:`aiohttp.ClientResponse`
        instance if you are using AsyncClient, otherwise
        it will be :class:`requests.Session`.
    message: :class:`str`
        The message of the error.
        Could be an empty string.
    status: :class:`int`
        The status code of the HTTP request.
        e.g. 404, 403, 500
    """

    def __init__(self, response: Response, message: Union[str, Dict[str, Any]]) -> None:
        self.response: Response = response
        self.status = response.status

        if isinstance(message, dict):
            self.code: int = message.get("code", 0)
            self.message: str = message.get("error_description", message.get("message"))
        else:
            self.code: int = 0
            self.message: str = message

        fmt = "{0.status} {0.reason} (error code: {1})"
        super().__init__(fmt.format(response, self.code))


class Forbidden(HTTPException):
    """Exception that's raised for when status code 403.

    Subclass of :exc:`HTTPException`
    """

    pass


class NotFound(HTTPException):
    """Exception that's raised for when status code 404.

    Subclass of :exc:`HTTPException`
    """

    pass


class DiscordServerError(HTTPException):
    """Exception that's raised for when a 500 range status code.

    Subclass of :exc:`HTTPException`
    """

    pass
