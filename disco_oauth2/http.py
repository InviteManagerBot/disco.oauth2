from __future__ import annotations

import aiohttp
import sys
import logging
import asyncio

from urllib.parse import quote as _quote

from . import __version__
from .errors import HTTPException, Forbidden, NotFound, DiscordServerError
from .utils import MISSING, json_or_text

from typing import (
    ClassVar,
    Iterable,
    Optional,
    TypeVar,
    overload,
    TYPE_CHECKING,
    Coroutine,
    Any,
    List,
)

if TYPE_CHECKING:
    from .types import (
        Snowflake,
        SnowflakeList,
        User,
        AccessToken as AccessTokenResponse,
        Member,
        PartialGuild as PartialGuildPayload,
        Connection as ConnectionPayload,
    )

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]
    Session = aiohttp.ClientSession

_log = logging.getLogger(__name__)

__all__ = ("AsyncHTTP",)


class Route:
    BASE: ClassVar[str] = "https://discord.com/api/v10"

    def __init__(self, method: str, path: str, **params: Any) -> None:
        self.method = method
        self.url = self.BASE + path

        if params:
            self.url = self.url.format_map(
                {k: _quote(v) if isinstance(v, str) else v for k, v in params.items()}
            )


class BaseHTTP:
    """Represents an HTTP client sending HTTP requests to the Discord API[oauth2]."""

    def __init__(
        self,
        *,
        client_id: int,
        client_secret: str,
        redirect_uri: str,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
    ) -> None:
        self.client_id = client_id
        self._client_secret = client_secret
        self.redirect_uri = redirect_uri

        # Proxy support
        self.proxy: Optional[str] = proxy
        self.proxy_auth: Optional[aiohttp.BasicAuth] = proxy_auth

    @overload
    def _create_session(self) -> Any:
        ...

    @overload
    def _create_session(self) -> Coroutine[Any, Any, aiohttp.ClientSession]:
        ...

    def _create_session(self) -> Any:
        raise NotImplementedError

    @overload
    def request(self, route: Route, **kwargs) -> Any:
        ...

    @overload
    def request(self, route: Route, **kwargs) -> Response[Any]:
        ...

    def request(self, route: Route, **kwargs) -> Any:
        raise NotImplementedError

    @overload
    def close(self) -> None:
        ...

    @overload
    def close(self) -> Coroutine[Any, Any, None]:
        ...

    def close(self) -> Any:
        raise NotImplementedError

    # Api methods

    def get_current_auth(self) -> Response[Any]:
        r = Route("GET", "/oauth2/@me")
        payload = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
        }

        return self.request(r, data=payload)

    def get_user(self, access_token: str) -> Response[User]:
        r = Route("GET", "/users/@me")
        headers = {"Authorization": f"Bearer {access_token}"}

        return self.request(r, headers=headers)

    def get_member(self, access_token: str, guild_id: Snowflake) -> Response[Member]:
        r = Route("GET", "/users/@me/guilds/{guild_id}/member", guild_id=guild_id)
        headers = {"Authorization": f"Bearer {access_token}"}

        return self.request(r, headers=headers)

    def add_user_guild(
        self,
        user_id: Snowflake,
        guild_id: Snowflake,
        access_token: str,
        bot_token: str,
        *,
        nick: Optional[str] = None,
        roles: Optional[SnowflakeList] = None,
        mute: Optional[bool] = False,
        deaf: Optional[bool] = False,
    ) -> Response[None]:
        headers = {"Authorization": bot_token}
        payload = {
            "access_token": access_token,
            "mute": mute,
            "deaf": deaf,
        }
        if nick:
            payload["nick"] = nick
        if roles:
            payload["roles"] = nick

        r = Route(
            "PUT",
            "/guilds/{guild_id}/members/{user_id}",
            guild_id=guild_id,
            user_id=user_id,
        )
        return self.request(r, data=payload, headers=headers)

    def get_user_guilds(self, access_token: str) -> Response[List[PartialGuildPayload]]:
        r = Route("GET", "/users/@me/guilds")
        headers = {"Authorization": f"Bearer {access_token}"}

        return self.request(r, headers=headers)

    def get_user_connections(
        self, access_token: str
    ) -> Response[List[ConnectionPayload]]:
        r = Route("GET", "/users/@me/connections")
        headers = {"Authorization": f"Bearer {access_token}"}

        return self.request(r, headers=headers)

    def refresh_token(self, refresh_token: str) -> Response[AccessTokenResponse]:
        r = Route("GET", "/oauth2/token")
        payload = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        return self.request(r, data=payload)

    def exchange_code(
        self, code: str, *, scopes: Optional[Iterable[str]] = None
    ) -> Response[AccessTokenResponse]:
        r = Route("POST", "/oauth2/token")
        payload = {
            "client_id": self.client_id,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        if scopes:
            payload["scope"] = list(scopes)

        return self.request(r, data=payload)


class AsyncHTTP(BaseHTTP):
    def __init__(
        self,
        connector: Optional[aiohttp.BaseConnector] = None,
        *,
        client_id: int,
        client_secret: str,
        redirect_uri: str,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        http_trace: Optional[aiohttp.TraceConfig] = None,
    ) -> None:
        super().__init__(
            proxy=proxy,
            proxy_auth=proxy_auth,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        self.connector: Optional[aiohttp.BaseConnector] = connector
        self.loop: Optional[asyncio.AbstractEventLoop] = loop
        self.http_trace: Optional[aiohttp.TraceConfig] = http_trace
        self.__session: aiohttp.ClientSession = self._create_session()

        user_agent = "OAuth2 (https://github.com/InviteManagerBot/disco.oauth2 {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )

    def _create_session(self) -> aiohttp.ClientSession:
        if self.connector is None:
            self.connector = aiohttp.TCPConnector(limit=0)

        return aiohttp.ClientSession(
            connector=self.connector,
            trace_configs=None if self.http_trace is None else [self.http_trace],
            loop=self.loop,
        )

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = route.url

        headers = {"User-Agent": self.user_agent, **kwargs.get("headers", {})}

        # discord OAuth2 api requires this Content-Type header
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        if self.proxy:
            kwargs["proxy"] = self.proxy
        if self.proxy_auth:
            kwargs["proxy_auth"] = self.proxy_auth

        # 5 tries
        for trie in range(5):
            async with self.__session.request(method, url, **kwargs) as resp:
                _log.debug("%s %s has returned %s", method, url, resp.status)

                data = await json_or_text(resp)
                status = resp.status

                if 300 > resp.status >= 200:
                    _log.debug("%s %s has received %s", method, url, data)
                    return data

                # rate limit handle
                if status == 429:
                    if not resp.headers.get("Via") or isinstance(data, str):
                        # Banned by Cloudflare more than likely.
                        raise HTTPException(resp, data)

                    retry_after_secs: int = data["retry_after"] / 1000
                    _log.warning(
                        "You are being rate limit, trying again after %.2f seconds",
                        retry_after_secs,
                    )

                    await asyncio.sleep(retry_after_secs)
                    _log.debug("Done sleeping for the rate limit, retrying...")
                    continue

                if status in (500, 502, 504):
                    try_after: int = 1 + trie * 2
                    _log.debug(
                        "Internal error received from %s, trying again after %s seconds",
                        url,
                        try_after,
                    )
                    await asyncio.sleep(try_after)

                if status == 403:
                    raise Forbidden(resp, data)
                elif status == 404:
                    raise NotFound(resp, data)
                elif status >= 500:
                    raise DiscordServerError(resp, data)
                else:
                    raise HTTPException(resp, data)

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()
            self.__session = MISSING
