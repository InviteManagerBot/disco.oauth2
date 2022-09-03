import aiohttp
import asyncio

from weakref import WeakValueDictionary
from typing import List, Literal, Optional

from .http import AsyncHTTP
from .token import AccessToken
from .user import User, PartialUser
from .utils import MISSING

__all__ = ("Client",)


class Client:
    """Represents a client that offers interaction to the discord OAuth2 API.

    Parameters
    -----------
    client_id: :class:`int`
        The OAuth2 application client id.
    client_secret: :class:`str`
        The OAuth2 application client secret.
    redirect_uri: :class:`str`
        The OAuth2 redirect url.
        This url must configurated from uri's at discord developer portal.
    scopes: Optional[List[:class:`str`]]
        List of OAuth2 scopes.
        Default ``None``.
    connector: Optional[:class:`aiohttp.BaseConnector`]
        A connector for aiohttp client API.
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.BaseConnector>`.
        Default ``None``.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The event loop of asyncio.
        This loop will be only used at the instance of :class:`aiohttp.ClientSession`.
        Default ``None``.
    proxy: Optional[:class:`str`]
        The proxy URL.
        Default ``None``.
    proxy_auth: Optional[:class:`aiohttp.BasicAuth`]
        Object that represents proxy HTTP Basic Authorization.
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.BasicAuth>`.
        Default ``None``.
    http_trace: Optional[:class:`aiohttp.TraceConfig`]
        The trace configuration to use for tracking HTTP requests the library does using ``aiohttp``.
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_advanced.html#client-tracing>`.
        Default ``None``.
    """

    def __init__(
        self,
        *,
        client_id: int,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        http_trace: Optional[aiohttp.TraceConfig] = None,
    ) -> None:
        self.client_id: int = client_id
        self._client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.scopes: List[str] = scopes or []
        self.http: AsyncHTTP = AsyncHTTP(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            connector=connector,
            loop=loop,
            proxy=proxy,
            proxy_auth=proxy_auth,
            http_trace=http_trace,
        )

    async def exchange_code(self, code: str) -> AccessToken:
        """Exchanges the code you receive from the OAuth2 redirect.

        Parameters
        ---------
        code: :class:`str`
            The code from the querystring.

        Returns
        -------
        :class:`AccessToken`
        """
        data = await self.http.exchange_code(code, scopes=self.scopes)
        return AccessToken(data)

    async def refresh_token(self, refresh_token: str) -> AccessToken:
        """Refreshes an access token.
        This can be useful to anticipate the expiration and refresh the token.

        Parameters
        ---------
        refresh_toke: :class:`str`
            The user's refresh token.

        Returns
        -------
        :class:`AccessToken`
        """
        data = await self.http.refresh_token(refresh_token)
        return AccessToken(data)

    async def fetch_user(self, access_token: AccessToken) -> User:
        """Fetch user's information from discord api using user's access token.

        You must have the scope `identify` to use this.
        To access user's email you must have the scope `email`.

        Parameters
        ----------
        access_token: :class:`AccessToken`
            The user's access token.

        Returns
        ------
        :class:`User`
        """
        data = await self.http.get_user(access_token.access_token)
        user = User(http=self.http, access_token=access_token, data=data)
        return user

    def get_oauth_url(
        self,
        *,
        prompt: str = MISSING,
        state: str = MISSING,
        response_type: Literal["code", "token"] = "code",
        disable_guild_select: bool = MISSING,
        guild_id: int = MISSING,
        permissions: int = MISSING,
    ) -> str:
        """Returns the OAuth2 URL to authorize this application.

        Parameters
        ----------
        prompt: :class:`bool`
            Controls how existing authorizations are handled, either consent or none.
            You must have scopes set to use this.
        state: :class:`str`
            A unique cryptographically secure hash.
            _<https://discord.com/developers/docs/topics/oauth2#state-and-security>
        response_type: Literal["code", "token"]
            The response type, either code or token.
            The `token` is for client-side web applications only.
            Defaults ``code``.
        disable_guild_select: :class:`bool`
            Disallows the user from changing the guild for the bot invite, either true or false.
            You must have the scope `bot` to use this.
        guild_id: :class:`bool`
            The guild id to pre-fill at authorization url.
            You must have the scope `bot` to use this.
        permissions: :class:`int`
            The permissions flags for the bot invite.
            You must have the scope `bot` to use this.
        """
        from urllib.parse import quote

        base = f"https://discord.com/api/oauth2/authorize?client_id={self.client_id}"

        if self.scopes:
            base += f"&scope={'+'.join(self.scopes)}"

        if prompt is not MISSING:
            base += f"&prompt={prompt}"
        if state is not MISSING:
            base += f"&state={quote(state)}"
        if "bot" in self.scopes:
            if disable_guild_select is not MISSING:
                base += f"&disable_guild_select={prompt}"
            if guild_id is not MISSING:
                base += f"&guild_id={guild_id}"
            if permissions is not MISSING:
                base += f"&permissions={permissions}"

        base += (
            f"&response_type={response_type}"
            f"&redirect_uri={quote(self.redirect_uri)}"
        )

        return base

    def get_user(self, id: int, /) -> Optional[User]:
        """Returns a user with the given ID

        Parameters
        ----------
        id: :class:`int`
            The user's id that you
            want to find.

        Returns
        -------
        Optional[:class:`User`]
            Returns ``None`` when there's no user with that id
            in the cache
        """
        return self._users.get(id)

    def get_partial_user(self, *, access_token: AccessToken) -> PartialUser:
        """Returns a partial user.

        This is useful if you have a access_token but don't want to do an API call
        to fetch it again.

        Note that this partial user class will not let you use methods that requires
        user information.

        Parameters
        ----------
        access_token: :class:`AccessToken`
            The user's access token.

        Returns
        ------
        :class:`PartialUser`
        """
        return PartialUser(http=self.http, access_token=access_token)

    async def close(self):
        """Closes and cleanup operations on the client."""
        await self.http.close()
