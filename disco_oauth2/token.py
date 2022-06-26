from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .types import AccessToken as AccessTokenPayload

    from typing_extensions import Self

__all__ = ("AccessToken",)


class AccessToken:
    """Represents a access token response information provided by discord.

    Attributes
    ----------
    access_token: :class:`str`
        The user's access token.
    token_type: :class:`str`
        The token type.
    refresh_token: :class:`str`
        The user's refresh token.
    expires_in: :class:`int`
        When this access token will expire (in seconds).
    """

    def __init__(self, data: AccessTokenPayload) -> None:
        self.access_token: str = data["access_token"]
        self.token_type: str = data["token_type"]
        self.refresh_token: str = data["refresh_token"]
        self.scope: str = data["scope"]
        self.expires_in: int = data["expires_in"]

    @property
    def expires_at(self) -> datetime:
        return datetime.now() - timedelta(seconds=self.expires_in)
