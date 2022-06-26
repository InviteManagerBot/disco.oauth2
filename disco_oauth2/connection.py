from __future__ import annotations

from typing import TYPE_CHECKING, List
from enum import Enum

from .integration import ServerIntegration

if TYPE_CHECKING:
    from .user import User
    from .types import (
        IntegrationType as ConnectionType,
        Connection as ConnectionPayload,
    )

__all__ = ("Connection",)


class Visibility(Enum):
    none = 0
    everyone = 1


class Connection:
    """Represents connection object that the user has attached.

    Attributes
    -----------
    id: :class:`int`
        The connection's unique id.
    name: :class:`str`
        The connection's name.
    type: :class:`str`
        The service of the connection (twitch, youtube).
    revoked: :class:`bool`
       If the connection is revoked.
    verified: :class:`bool`
        If the connection is verified.
    friend_sync: :class:`bool`
        If friend sync is enabled for this connection.
    show_activity: :class:`bool`
        If activities related to this connection
        will be shown in presence updates
    visibility: :class:`Visibility`
        Visibility of this connection
    """

    __slots__ = (
        "id",
        "name",
        "type",
        "revoked",
        "integrations",
        "verified",
        "friend_sync",
        "show_activity",
        "visibility",
        "user",
    )

    def __init__(self, data: ConnectionPayload, user: User) -> None:
        self.user: User = user
        self.id = data["id"]
        self.name = data["name"]
        self.type: ConnectionType = data["type"]
        self.revoked: bool = data.get("revoked", False)
        self.integrations: List[ServerIntegration] = [
            ServerIntegration(x, user=user) for x in data.get("integrations", [])
        ]
        self.verified: bool = data["verified"]
        self.friend_sync: bool = data["friend_sync"]
        self.show_activity: bool = data["show_activity"]
        self.visibility: Visibility = Visibility(data["visibility"])

    def __repr__(self) -> str:
        return f"<Connection id={self.id} name={self.name!r} type={self.type!r}>"

    def __str__(self) -> str:
        return self.name
