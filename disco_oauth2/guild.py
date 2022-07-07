from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from .member import Member
from .flags import Permissions

if TYPE_CHECKING:
    from .types import PartialGuild as PartialGuildPayload
    from .http import AsyncHTTP
    from .user import User

__all__ = ("Guild",)


class Guild:
    """Represents a Discord partial guild.

    This is referred to as a "server" in the official Discord UI.

    .. container:: operations

        .. describe:: x == y

            Checks if two guilds are equal.

        .. describe:: x != y

            Checks if two guilds are not equal.

        .. describe:: hash(x)

            Returns the guild's hash.

        .. describe:: str(x)

            Returns the guild's name.

    Attributes
    ----------
    id: :class:`int`
        The guild id.
    name: :class:`str`
        The guild name.
    permissions: Optional[:class:`Permissions`]
        An Permissions class that represents
        the permissions of the user in the guild.
    features: Optional[List[:class:`str`]]
        A list of features that the guild has.
    """

    def __init__(self, data: PartialGuildPayload, user: User, http: AsyncHTTP) -> None:
        self._http: AsyncHTTP = http
        self._user: User = user
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self._icon_hash: Optional[str] = data.get("icon")
        self._is_owner: Optional[bool] = data.get("owner")
        self._permissions: int = int(data.get("permissions", 0))
        self.features: Optional[List[str]] = data.get("features")

    def __repr__(self) -> str:
        return f"<Guild id={self.id} name={self.name!r}>"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Guild) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return self.id >> 22

    @property
    def permissions(self) -> Permissions:
        """:class:`Permissions`: Returns the resolved permissions that the oauth2 user has in this guild."""
        return Permissions(self._permissions)

    @property
    def icon(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the guild's icon url, if available."""
        if not self._icon_hash:
            return None

        animated = self._icon_hash.startswith("a_")
        fmt = "gif" if animated else "png"
        return f"https://cdn.discordapp.com/icons/{self.id}/{self._icon_hash}.{fmt}?size=1024"

    @property
    def is_owner(self) -> Optional[bool]:
        """Optional[:class:`str`]: Returns if the current user is the owner of the guild."""
        return self._is_owner
