from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .utils import parse_time
from .flags import Permissions

if TYPE_CHECKING:
    from datetime import datetime

    from .user import User
    from .guild import Guild
    from .types import Member as MemberPayload, SnowflakeList


__all__ = ("Member",)


class Member:
    """Represents a Discord member to a :class:`Guild`.

    .. container:: operations

        ..  describe:: x == y

            Compare the ids of the two members and verify that they are the same.

        .. describe:: x != y

            Compare the ids of the two members and verify that they are the different.

        .. describe:: hash(x)

            Return the member's hash.

        .. describe:: str(x)

            Returns the member's id with discriminator.

    Attributes
    ----------
    user: :class:`User`
        The user representation of this member.
    guild_id: :class:`int`
        The guild ID that the user is member of.
    nick: :class:`str`
        The guild specific nickname of the user.
    roles: :class:`SnowflakeList`
        The list of role ids that the member has
    joined_at: :class:`datetime.datetime`
        An aware datetime object that specifies the date and time in UTC that the member joined the guild.
    premium_since: Optional[:class:`datetime.datetime`]
        An aware datetime object that specifies the date andtime in UTC that the member "Nitro boost" the guild.
        This could be ``None``.
    deaf: :class:`bool`
        If the user is deafened in voice channels.
    mute: :class:`bool`
        If the user is muted in voice channels
    pending: :class:`bool`
        If the user has not yet passed the guild's Membership Screening requirements.
    timed_out_until: Optional[:class:`datetime.datetime`]
        An aware datetime object that specifies the date and time in UTC that the user's time out will expire.
        This is ``None`` when the user is not timed out.
    """

    __slots__ = (
        "user",
        "guild_id",
        "nick",
        "_avatar_hash",
        "roles",
        "joined_at",
        "premium_since",
        "deaf",
        "mute",
        "pending",
        "_permissions",
        "timed_out_until",
    )

    def __init__(self, data: MemberPayload, user: User, guild_id: int) -> None:
        self.user: User = user

        # Update the user object with new data
        try:
            self.user._update(data["user"])
        except KeyError:
            pass

        self.guild_id: int = guild_id
        self.nick: Optional[str] = data.get("nick")
        self._avatar_hash: Optional[str] = data.get("avatar")
        self.roles: SnowflakeList = data["roles"]
        self.joined_at: datetime = parse_time(data["joined_at"])
        self.premium_since: Optional[datetime] = parse_time(data.get("premium_since"))
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: Optional[bool] = data.get("pending")
        self._permissions: int = int(data.get("permissions", 0))
        self.timed_out_until: Optional[datetime] = parse_time(
            data.get("communication_disabled_until")
        )

    def __str__(self) -> str:
        return str(self.user)

    def __repr__(self) -> str:
        return (
            f"<Member id={self.user.id} name={self.user.name!r} discriminator={self.user.discriminator!r}"
            f" bot={self.user.bot} nick={self.nick!r} guild_id={self.guild_id}>"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Member) and other.user.id == self.user.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.user)

    @property
    def permissions(self) -> Permissions:
        """:class:`Permissions`: Returns the resolved permissions that the oauth2 user has in this guild."""
        return Permissions(self._permissions)

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string format to mention this member in discord."""
        return f"<@{self.user.id}>"

    @property
    def display_name(self) -> str:
        """:class:`str`: Returns the user's display name."""
        return self.nick or self.user.name

    @property
    def guild_avatar_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the link of cdn for the avatar the member has."""
        if self._avatar_hash is None:
            return None

        animated = self._avatar_hash.startswith("a_")
        fmt = "gif" if animated else "png"
        return f"https://cdn.discordapp.com/guilds/{self.guild_id}/users/{self.user.id}/avatars/{self._avatar_hash}.{fmt}?size=1024"

    @property
    def display_avatar(self) -> str:
        """:class:`str`: Returns the member's display avatar."""
        return self.guild_avatar_url or self.user.display_avatar
