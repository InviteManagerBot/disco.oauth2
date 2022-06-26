from typing import TypedDict, List
from .integration import ServerIntegration
from .integration import IntegrationType as ConnectionType


class _OptionalConnection(TypedDict, total=False):
    revoked: bool
    integrations: List[ServerIntegration]


class Connection(_OptionalConnection):
    id: int
    name: str
    type: ConnectionType
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: int
