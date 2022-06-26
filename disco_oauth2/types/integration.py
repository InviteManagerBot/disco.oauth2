from typing import TypedDict, Literal, TypeAlias
from .snowflake import Snowflake
from .user import User

IntegrationType: TypeAlias = Literal[
    "youtube",
    "xbox",
    "twitter",
    "twitch",
    "steam",
    "spotify",
    "reddit",
    "playstation",
    "github",
    "facebook",
    "battlenet",
]


class IntegrationAccount(TypedDict):
    id: int
    name: str


class _OptionalIntegration(TypedDict, total=False):
    enabled: bool
    syncing: bool
    role_id: Snowflake
    enable_emoticons: bool
    expire_behavior: int
    expire_grace_period: int
    user: User
    synced_at: str
    subscriber_count: int
    revoked: bool


class ServerIntegration(_OptionalIntegration):
    id: int
    name: str
    type: IntegrationType
    account: IntegrationAccount
