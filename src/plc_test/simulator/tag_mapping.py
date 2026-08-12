from dataclasses import dataclass

from plc_test.core.tag import Tag
from plc_test.core.tag_mapping import TagMapping


@dataclass(frozen=True)
class SimulatedTagMapping(TagMapping):
    """Mapping for a tag in the simulated PLC."""

    identifier: str

    def get_address(self) -> str:
        """Return the simulated tag identifier."""
        return self.identifier
