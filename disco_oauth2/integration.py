from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from enum import Enum

from .utils import try_enum, parse_time
from .appinfo import IntegrationApp

if TYPE_CHECKING:
    from .types import (
        ServerIntegration as ServerIntegrationPayload,
        IntegrationType,
        IntegrationAccount as IntegrationAccountPayload,
        Snowflake,
        IntegrationApp as IntegrationAppPayload,
        IntegrationAccount as IntegrationAccountPayload,
    )
    from .user import User
    from datetime import datetime

__all__ = ("ExpireBehavior", "IntegrationAccount", "ServerIntegration")


class ExpireBehavior(Enum):
    remove_role = 0
    kick = 1


class IntegrationAccount:
    """Represents integration account.

    Attributes
    ----------
    id: :class:`int`
        Id of the account.
    name: :class:`str`
        Name of the account.
    """

    __slots__ = ("id", "name")

    def __init__(self, data: IntegrationAccountPayload) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]

    def __repr__(self) -> str:
        return f"<IntegrationAccount id={self.id} name={self.name!r}>"


class ServerIntegration:
    """Represents discord server integrations.

    Attributes
    ----------
    id: :class:`int`
        The integration unique id.
    name: :class:`str`
        The integration name.
    type: :class:`IntegrationType`
        The integration type (twitch, youtube, discord, ...).
    enabled: :class:`bool`
        If this integration enabled.
    syncing: :class:`bool`
        If this integration syncing.
    role_id: :class:`int`
        role id that this integration uses for "subscribers".
    enable_emoticons: Optional[:class:`bool`]
        If emoticons should be synced for this integration (twitch only currently).
    expire_behavior: Optional[:class:`ExpireBehavior`]
        The behavior of expiring subscribers (remove_role or kick).
    expire_grace_period: :class:`int`
        The grace period (in days) before expiring subscribers.
    user: :class:`User`
        User for this integration.
    account: :class:`IntegrationAccount`
        Integration account information.
    synced_at: Optional[:class:`datetime.datetime`]
        When this integration was last synced.
    subscriber_count: Optional[:class:`int`]
        How many subscribers this integration has.
    revoked: :class:`bool`
        If has this integration been revoked.
    application: Optional[:class:`IntegrationApp`]
        The bot/OAuth2 application for discord integrations, if available.
    """

    __slots__ = (
        "user",
        "id",
        "name",
        "type",
        "enabled",
        "syncing",
        "role_id",
        "enable_emoticons",
        "expire_behavior",
        "expire_grace_period",
        "account",
        "synced_at",
        "subscriber_count",
        "revoked",
        "application",
    )

    def __init__(self, data: ServerIntegrationPayload, user: User) -> None:
        self.user: User = user
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.type: IntegrationType = data["type"]
        self.enabled: bool = data.get("enabled", False)
        self.syncing: bool = data.get("syncing", False)
        self.role_id: Optional[Snowflake] = data.get("role_id")
        self.enable_emoticons: Optional[bool] = data.get("enable_emoticons")
        self.expire_behavior: Optional[ExpireBehavior] = try_enum(
            ExpireBehavior, data.get("expire_behavior")
        )
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")
        self.account: IntegrationAccount = IntegrationAccount(data["account"])
        self.synced_at: Optional[datetime] = parse_time(data.get("synced_at"))
        self.subscriber_count: Optional[int] = data.get("subscriber_count")
        self.revoked: bool = data.get("revoked", False)
        application: Optional[IntegrationAppPayload] = data.get("application")
        self.application: Optional[IntegrationApp] = (
            IntegrationApp(application) if application else None
        )

    def __repr__(self) -> str:
        return f"<Integration id={self.id} name={self.name!r}>"

    def __str__(self) -> str:
        return self.name
