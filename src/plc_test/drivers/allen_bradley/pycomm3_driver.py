from typing import Any

from pycomm3 import LogixDriver

from plc_test.core.plc_interface import PLCInterface
from plc_test.core.exceptions import (
    PLCConnectionError,
    PLCReadError,
    PLCWriteError,
)


class AllenBradleyPLC(PLCInterface):
    """Allen-Bradley ControlLogix/CompactLogix PLC driver."""

    def __init__(
        self,
        ip_address: str,
        slot: int | None = None,
    ) -> None:
        self.ip_address = ip_address

        if slot is not None:
            self.path = f"{ip_address}/{slot}"
        else:
            self.path = ip_address

        self.client: LogixDriver | None = None
        self._connected = False

    def connect(self) -> None:
        """Connect to the Allen-Bradley PLC."""

        try:
            self.client = LogixDriver(self.path)
            self.client.open()

            self._connected = True

        except Exception as exc:
            self._connected = False
            self.client = None

            raise PLCConnectionError(
                f"Failed to connect to Allen-Bradley PLC at "
                f"{self.path}: {exc}"
            ) from exc

    def disconnect(self) -> None:
        """Disconnect from the Allen-Bradley PLC."""

        if self.client is not None:
            try:
                self.client.close()
            finally:
                self._connected = False
                self.client = None

    def is_connected(self) -> bool:
        """Return True if the PLC is connected."""

        return self._connected

    def read_tag(self, tag: str) -> Any:
        """Read an Allen-Bradley controller tag."""

        if not self._connected or self.client is None:
            raise PLCReadError(
                "Cannot read tag because the PLC is not connected."
            )

        try:
            result = self.client.read(tag)

            if result.error:
                raise PLCReadError(
                    f"Failed to read tag '{tag}': {result.error}"
                )

            return result.value

        except PLCReadError:
            raise

        except Exception as exc:
            raise PLCReadError(
                f"Failed to read Allen-Bradley tag '{tag}': {exc}"
            ) from exc

    def write_tag(self, tag: str, value: Any) -> None:
        """Write an Allen-Bradley controller tag."""

        if not self._connected or self.client is None:
            raise PLCWriteError(
                "Cannot write tag because the PLC is not connected."
            )

        try:
            result = self.client.write((tag, value))

            if result.error:
                raise PLCWriteError(
                    f"Failed to write tag '{tag}': {result.error}"
                )

        except PLCWriteError:
            raise

        except Exception as exc:
            raise PLCWriteError(
                f"Failed to write Allen-Bradley tag '{tag}': {exc}"
            ) from exc
