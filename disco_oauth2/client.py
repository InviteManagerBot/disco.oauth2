import aiohttp

from typing import Literal, Optional, Iterable

from .http import AsyncHTTP
from .token import AccessToken
from .user import User, PartialUser
from .utils import MISSING
from .types.snowflake import Snowflake

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
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.BaseConnector>`_.
        Default ``None``.
    proxy: Optional[:class:`str`]
        The proxy URL.
        Default ``None``.
    proxy_auth: Optional[:class:`aiohttp.BasicAuth`]
        Object that represents proxy HTTP Basic Authorization.
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.BasicAuth>`_.
        Default ``None``.
    http_trace: Optional[:class:`aiohttp.TraceConfig`]
        The trace configuration to use for tracking HTTP requests the library does using ``aiohttp``.
        `aiohttp documentation <https://docs.aiohttp.org/en/stable/client_advanced.html#client-tracing>`_.
        Default ``None``.
    """

    def __init__(
        self,
        *,
        client_id: int,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[Iterable[str]] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        http_trace: Optional[aiohttp.TraceConfig] = None,
    ) -> None:
        self.client_id: int = client_id
        self._client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.scopes: Iterable[str] = scopes or ()
        self.http: AsyncHTTP = AsyncHTTP(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            connector=connector,
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

    async def revoke_token(self, token: str) -> None:
        """Revokes a token, token can be either an access token or an refresh token.
        This can be useful to invalidate the previous token.

        `RFC7009 <https://www.rfc-editor.org/rfc/rfc7009>`_.

        .. note::
            Invalid tokens **do not** cause an error response.

        Parameters
        ---------
        token: :class:`str`
            The refresh or access token that will get revoked.
        """
        await self.http.revoke_token(token)

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
        prompt: Literal["none", "consent"] = MISSING,
        state: str = MISSING,
        response_type: Literal["code", "token"] = "code",
        disable_guild_select: bool = MISSING,
        guild_id: Snowflake = MISSING,
        permissions: int = MISSING,
        scopes: Iterable[str] = MISSING,
        redirect_uri: str = MISSING,
    ) -> str:
        """Returns the OAuth2 URL to authorize this application.

        Parameters
        ----------
        prompt: :class:`str`
            Controls how existing authorizations are handled, either consent or none.
            You must have scopes set to use this.
        state: :class:`str`
            A unique cryptographically secure hash.
            `discord documentation <https://discord.com/developers/docs/topics/oauth2#state-and-security>`_
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
        scopes: Iterable[:class:`str`]
            An optional valid list of scopes.
            Defaults to ``self.scopes``.

            .. versionadded:: 1.3
        redirect_uri: :class:`str`
            An optional valid redirect URI.
            Defaults ``self.redirect_uri``

            .. versionadded:: 1.3

        Returns
        -------
            The OAuth2 URL with all the received parameters.
        """
        from urllib.parse import quote

        base = f"https://discord.com/api/oauth2/authorize?client_id={self.client_id}"
        scopes = scopes or self.scopes
        redirect_uri = redirect_uri or self.redirect_uri

        if scopes:
            base += f"&scope={'+'.join(scopes)}"

        if prompt is not MISSING:
            base += f"&prompt={prompt}"
        if state is not MISSING:
            base += f"&state={quote(state)}"
        if redirect_uri is not MISSING:
            base += f"&redirect_uri={quote(redirect_uri)}"
        if "bot" in scopes:
            if disable_guild_select is not MISSING:
                base += f"&disable_guild_select={prompt}"
            if guild_id is not MISSING:
                base += f"&guild_id={guild_id}"
            if permissions is not MISSING:
                base += f"&permissions={permissions}"

        base += f"&response_type={response_type}"

        return base

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
