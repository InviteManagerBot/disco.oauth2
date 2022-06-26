from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .types import (
        IntegrationApp as IntegrationAppPayload,
    )

__all__ = ("IntegrationApp",)


class IntegrationApp:
    """Represents the integration application provided by Discord.

    Attributes
    ----------
    id: :class:`int`
        The application unique id.
    name: :class:`str`
        The application name.
    description: :class:`str`
        The description of the app.
    """

    __slots__ = (
        "id",
        "name",
        "_icon_hash",
        "description",
        "bot",
    )

    def __init__(self, data: IntegrationAppPayload) -> None:
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self._icon_hash: Optional[str] = data.get("icon")
        self.description: str = data["description"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} description={self.description!r}"

    @property
    def icon(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the app's icon url, if available."""
        if not self._icon_hash:
            return None
        return f"https://cdn.discordapp.com/app-icons/{self.id}/{self._icon_hash}.png?size=1024"
