from abc import ABC, abstractmethod
from typing import Any

from .tag_registry import TagRegistry


class PLCInterface(ABC):
    """Vendor-neutral interface for communicating with a PLC."""

    def __init__(self, tag_registry: TagRegistry) -> None:
        self.tag_registry = tag_registry

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the PLC."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection to the PLC."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if the PLC is currently connected."""
        pass

    @abstractmethod
    def read_tag(self, tag_name: str) -> Any:
        """Read a logical tag from the PLC."""
        pass

    @abstractmethod
    def write_tag(self, tag_name: str, value: Any) -> None:
        """Write a value to a logical tag."""
        pass
