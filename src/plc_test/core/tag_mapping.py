from abc import ABC, abstractmethod
from dataclasses import dataclass

from .tag import Tag


@dataclass(frozen=True)
class TagMapping(ABC):
    """Maps a logical Tag to a vendor-specific PLC address."""

    tag: Tag

    @abstractmethod
    def get_address(self) -> str:
        """Return the vendor-specific PLC address."""
        pass
