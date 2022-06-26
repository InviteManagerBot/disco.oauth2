from typing import TypedDict

class AccessToken(TypedDict):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: str