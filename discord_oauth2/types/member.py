from typing import TypedDict, Optional
from .snowflake import SnowflakeList
from .user import User

class PartialMember(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: bool
    mute: bool

class Member(PartialMember, total=False):
    avatar: str
    user: User
    nick: str
    premium_since: Optional[str]
    pending: bool
    permissions: str
    communication_disabled_until: str