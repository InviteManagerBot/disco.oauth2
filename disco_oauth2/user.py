from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from .guild import Guild
from .connection import Connection
from .flags import UserFlags
from .utils import snowflake_time
from .member import Member

if TYPE_CHECKING:
    from .types.user import PartialUser as UserPayload
    from .http import AsyncHTTP
    from .token import AccessToken
    from .types import Snowflake

    from datetime import datetime


__all__ = ("BaseUser", "User", "PartialUser")


class BaseUser:
    __slots__ = (
        "id",
        "name",
        "discriminator",
        "email",
        "mfa_enabled",
        "locale",
        "verified",
        "bot",
        "system",
        "_http",
        "_access_token",
        "_avatar_hash",
        "_banner_hash",
        "_accent_colour",
        "_public_flags",
        "_flags",
        "guilds",
        "connections",
    )

    def __init__(
        self, *, http: AsyncHTTP, access_token: AccessToken, data: UserPayload
    ) -> None:
        self._http: AsyncHTTP = http
        self._access_token: AccessToken = access_token
        self._update(data)

        self.guilds: List[Guild] = []
        self.connections: List[Connection] = []

    def _update(self, data: UserPayload):
        self.id: int = int(data["id"])
        self.name: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.email: Optional[str] = data.get("email", None)
        self._avatar_hash: Optional[str] = data["avatar"]
        self._banner_hash: Optional[str] = data.get("banner", None)
        self._accent_colour: Optional[int] = data.get("accent_color", None)
        self._public_flags: int = data.get("public_flags", 0)
        self._flags: int = data.get("flags", 0)
        self.mfa_enabled: bool = data.get("mfa_enabled", False)
        self.locale: Optional[str] = data.get("locale")
        self.verified: bool = data.get("verified", False)
        self.bot: bool = data.get("bot", False)
        self.system: bool = data.get("system", False)

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} discriminator={self.discriminator!r} bot={self.bot}>"

    def __str__(self) -> str:
        return f"{self.id}#{self.discriminator}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseUser) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return self.id >> 22

    @property
    def flags(self) -> UserFlags:
        """:class:`Permissions`: Returns the resolved flags of the user."""
        return UserFlags(self._flags)

    @property
    def public_flags(self) -> UserFlags:
        """:class:`Permissions`: Returns the resolved public flags of the user."""
        return UserFlags(self._public_flags)

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the link of cdn for the avatar the user has."""
        if self._avatar_hash is None:
            return None

        animated = self._avatar_hash.startswith("a_")
        fmt = "gif" if animated else "png"
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self._avatar_hash}.{fmt}"

    @property
    def default_avatar(self) -> str:
        """:class:`str`: Returns the default avatar for a given user.
        This is calculated by the user's discriminator.
        """
        index: int = int(self.discriminator) % 5
        return f"https://cdn.discordapp.com/embed/avatars/{index}.png"

    @property
    def display_avatar(self) -> str:
        """:class:`str`: Returns the user's display avatar.

        This method is similar to avatar_url, but
        if the user doesn't have an avatar it will give the default avatar.
        """
        return self.avatar_url or self.default_avatar

    @property
    def banner(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the user's banner asset, if available."""
        if self._banner_hash is None:
            return None

        animated = self._banner_hash.startswith("a_")
        fmt = "gif" if animated else "png"
        return f"https://cdn.discordapp.com/banners/{self.id}/{self._banner_hash}.{fmt}"

    @property
    def accent_colour(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the user's accent colour, if applicable.

        .. note::
            This property will return the color in hex format.
        """
        return f"#{self._accent_colour:0>6x}"

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string format to mention this user in discord."""
        return f"<@{self.id}>"

    @property
    def created_at(self) -> datetime:
        """:class:`datetime.datetime`: Returns the date of when the user account was created in UTC."""
        return snowflake_time(self.id)


class User(BaseUser):
    """Represents your Discord user that contains information from the OAuth2 API.

    .. container:: operations

        ..  describe:: x == y

            Compare the ids of the two users and verify that they are the same.

        .. describe:: x != y

            Compare the ids of the two users and verify that they are the different.

        .. describe:: hash(x)

            Return the user's hash.

        .. describe:: str(x)

            Returns the user's id with discriminator.

    Attributes
    -----------
    id: :class:`int`
        The user's unique id.
    name: :class:`str`
        The user's username.
    discriminator: :class:`str`
        The user's discriminator.
    email: Optional[:class:`str`]
        The user's email.
    bot: :class:`bool`
        If the current user is a bot account.
    system: :class:`bool`
        If the user is a system user.
    verified: :class:`bool`
        If the user's email is verified.
    locale: Optional[:class:`str`]
        The IETF language tag used to identify the language the user is using.
    mfa_enabled: :class:`bool`
        Specifies if the user has MFA turned on.
    """

    async def refresh(self) -> AccessToken:
        """Refreshes the access token for the user.

        Returns
        -------
        :class:`AccessToken`
        """
        access_token = self._access_token.access_token
        data = await self._http.refresh_token(refresh_token=access_token)
        self._access_token = AccessToken(data)
        return self._access_token

    async def add_guild(
        self,
        guild: Guild,
        bot_token: str,
        *,
        nick: Optional[str] = None,
        roles: Optional[List[Snowflake]] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
    ) -> None:
        """Adds a user to the guild.

        You must have the scope `guilds.join` to use this.

        Parameters
        ---------
        guild: :class:`.Guild`
            Guild that the user will join.
        bot_token: :class:`str`
            A bot token that is in the target guild.
            Discord requires a bot that you have a bot
            that is in the target guild you want to add the user.
        nick: Optional[:class:`str`]
            Value to set user's nickname to.
        roles: Optional[List[:class:`int`]]
            A list of role ids that will be added
            to the member.
        mute: Optional[:class:`bool`]
            Whether the user is muted in voice channels
        deaf: Optional[:class:`bool`]
            Whether the user is deafened in voice channels
        """
        await self._http.add_user_guild(
            self.id,
            guild.id,
            self._access_token.access_token,
            bot_token,
            nick=nick,
            roles=roles,
            mute=mute,
            deaf=deaf,
        )

    async def fetch_guilds(self) -> List[Guild]:
        """Fetch a list of partial guilds that the user is a member of.

        You must have the scope `guilds` to use this.

        Returns
        -------
        List[:class:`.Guild`]
        """
        data = await self._http.get_user_guilds(self._access_token.access_token)
        self.guilds = [Guild(data=x, user=self, http=self._http) for x in data]
        return self.guilds

    async def fetch_connections(self) -> List[Connection]:
        """Fetch a list of connections of the user.

        You must have the scope `connections` to use this.

        Returns
        -------
        List[:class:`Connection`]
        """
        data = await self._http.get_user_connections(self._access_token.access_token)
        self.connections = [Connection(x, self) for x in data]
        return self.connections

    async def fetch_member(self, guild_id: int) -> Member:
        """Fetch the user's object member from guild ID.

        You must have the scope `guilds.members.read` to use this.

        Parameters
        ----------
        guild_id: :class:`int`
            The guild's ID that the user is member of

        Returns
        --------
        :class:`Member`
        """
        data = await self._http.get_member(self._access_token.access_token, guild_id)
        return Member(data, self, guild_id)


class PartialUser(User):
    """Represents a partial user

    Note that this class is trimmed down and has no rich attributes.

    .. container:: operations

        ..  describe:: x == y

            Compare the ids of the two users and verify that they are the same.

        .. describe:: x != y

            Compare the ids of the two users and verify that they are the different.

        .. describe:: hash(x)

            Return the user's hash.
    """

    __slots__ = ("_http", "_access_token", "id")

    def __init__(self, *, http: AsyncHTTP, access_token: AccessToken) -> None:
        self._http = http
        self._access_token = access_token
        self.id = 0

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    async def add_guild(self, *args, **kwargs):
        # This method requires user id
        raise NotImplementedError
