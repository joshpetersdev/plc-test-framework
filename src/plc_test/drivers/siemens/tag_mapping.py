from dataclasses import dataclass

from plc_test.core.tag import Tag
from plc_test.core.tag_mapping import TagMapping


@dataclass(frozen=True)
class SiemensTagMapping(TagMapping):
    db_number: int
    byte_offset: int
    bit_offset: int | None = None
    size: int = 1

    def get_address(self) -> str:
        if self.bit_offset is not None:
            return (
                f"DB{self.db_number}.DBX"
                f"{self.byte_offset}.{self.bit_offset}"
            )

        return f"DB{self.db_number}.DBB{self.byte_offset}"
