from dataclasses import dataclass
from enum import Enum
from typing import Any


class TagDataType(Enum):
    BOOL = "BOOL"
    INT = "INT"
    DINT = "DINT"
    UINT = "UINT"
    UDINT = "UDINT"
    REAL = "REAL"
    LREAL = "LREAL"
    BYTE = "BYTE"
    WORD = "WORD"
    DWORD = "DWORD"
    STRING = "STRING"


class TagAccess(Enum):
    READ_ONLY = "read_only"
    WRITE_ONLY = "write_only"
    READ_WRITE = "read_write"


@dataclass(frozen=True)
class Tag:
    name: str
    data_type: TagDataType
    access: TagAccess = TagAccess.READ_WRITE
    description: str = ""

    def validate_value(self, value: Any) -> bool:
        """Return True if value is compatible with this tag's data type."""

        expected_type = {
            TagDataType.BOOL: bool,
            TagDataType.INT: int,
            TagDataType.DINT: int,
            TagDataType.UINT: int,
            TagDataType.UDINT: int,
            TagDataType.REAL: float,
            TagDataType.LREAL: float,
            TagDataType.BYTE: int,
            TagDataType.WORD: int,
            TagDataType.DWORD: int,
            TagDataType.STRING: str,
        }[self.data_type]

        return isinstance(value, expected_type)
