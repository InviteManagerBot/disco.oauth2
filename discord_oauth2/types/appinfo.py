from typing import TypedDict, Optional
from .user import User
from .snowflake import Snowflake

class IntegrationAccount(TypedDict):
    id: Snowflake
    name: str

class _OptionalIntegrationApp(TypedDict, total=False):
    bot: User
    
class IntegrationApp(_OptionalIntegrationApp):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str