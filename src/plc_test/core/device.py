from abc import ABC
from typing import Any

from .plc_interface import PLCInterface
from .tag import Tag
from .exceptions import TagNotFoundError


class Device(ABC):
    """Base class for a PLC-controlled device."""

    def __init__(
        self,
        name: str,
        plc: PLCInterface,
    ) -> None:
        self.name = name
        self.plc = plc

    def read_tag(self, tag_name: str) -> Any:
        """Read a tag associated with this device."""
        return self.plc.read_tag(tag_name)

    def write_tag(
        self,
        tag_name: str,
        value: Any,
    ) -> None:
        """Write a value to a tag associated with this device."""
        self.plc.write_tag(tag_name, value)
