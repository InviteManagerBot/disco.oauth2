from .snowflake import Snowflake
from typing import Literal, TypedDict


class PartialUser(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: str | None


PremiumType = Literal[0, 1, 2]


class User(PartialUser, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    local: str
    verified: bool
    email: str | None
    flags: int
    premium_type: PremiumType
    public_flags: int
