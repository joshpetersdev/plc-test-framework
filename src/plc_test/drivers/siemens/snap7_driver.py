from typing import Any

from s7commplus import Client

from plc_test.core.plc_interface import PLCInterface
from plc_test.core.exceptions import (
    PLCConnectionError,
    PLCReadError,
    PLCWriteError,
)


class SiemensPLC(PLCInterface):
    """Siemens S7-1200/1500 PLC driver using S7CommPlus."""

    def __init__(
        self,
        ip_address: str,
        tag_map: dict[str, tuple[int, int, int]],
    ) -> None:
        self.ip_address = ip_address
        self.tag_map = tag_map
        self.client = Client()
        self._connected = False

    def connect(self) -> None:
        """Connect to the Siemens PLC."""

        try:
            self.client.connect(self.ip_address)
            self._connected = True

        except Exception as exc:
            self._connected = False
            raise PLCConnectionError(
                f"Failed to connect to Siemens PLC at "
                f"{self.ip_address}: {exc}"
            ) from exc

    def disconnect(self) -> None:
        """Disconnect from the Siemens PLC."""

        if self._connected:
            try:
                self.client.disconnect()
            finally:
                self._connected = False

    def is_connected(self) -> bool:
        """Return True if the PLC is connected."""

        return self._connected

    def read_tag(self, tag: str) -> Any:
        """Read a tag from the Siemens PLC."""

        if not self._connected:
            raise PLCReadError(
                "Cannot read tag because the PLC is not connected."
            )

        try:
            db_number, byte_offset, size = self._get_address(tag)

            data = self.client.db_read(
                db_number,
                byte_offset,
                size,
            )

            return data

        except Exception as exc:
            raise PLCReadError(
                f"Failed to read Siemens tag '{tag}': {exc}"
            ) from exc

    def write_tag(self, tag: str, value: Any) -> None:
        """Write a tag to the Siemens PLC."""

        if not self._connected:
            raise PLCWriteError(
                "Cannot write tag because the PLC is not connected."
            )

        try:
            db_number, byte_offset, size = self._get_address(tag)

            data = self._encode_value(value, size)

            self.client.db_write(
                db_number,
                byte_offset,
                data,
            )

        except Exception as exc:
            raise PLCWriteError(
                f"Failed to write Siemens tag '{tag}': {exc}"
            ) from exc

    def _get_address(
        self,
        tag: str,
    ) -> tuple[int, int, int]:
        """Return DB number, byte offset, and size for a tag."""

        try:
            return self.tag_map[tag]
        except KeyError as exc:
            raise PLCReadError(
                f"No Siemens address configured for tag '{tag}'."
            ) from exc

    @staticmethod
    def _encode_value(value: Any, size: int) -> bytes:
        """Convert a Python value into bytes for the PLC."""

        if isinstance(value, bool):
            return bytes([1 if value else 0])

        if isinstance(value, int):
            return value.to_bytes(
                size,
                byteorder="big",
                signed=True,
            )

        if isinstance(value, float):
            import struct

            if size == 4:
                return struct.pack(">f", value)

            if size == 8:
                return struct.pack(">d", value)

        if isinstance(value, bytes):
            if len(value) != size:
                raise ValueError(
                    f"Expected {size} bytes, received {len(value)}."
                )

            return value

        raise TypeError(
            f"Unsupported PLC value type: {type(value).__name__}"
        )
