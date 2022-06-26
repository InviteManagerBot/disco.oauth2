from typing import TypedDict, List


class PartialGuild(TypedDict):
    id: int
    name: str
    icon: str
    owner: bool
    permissions: str
    features: List[str]
