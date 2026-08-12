from plc_test.core.device import Device


class Pump(Device):
    """Represents a PLC-controlled pump."""

    def start(self) -> None:
        """Command the pump to start."""
        self.write_tag("PumpStart", True)

    def stop(self) -> None:
        """Command the pump to stop."""
        self.write_tag("PumpStop", True)

    def reset(self) -> None:
        """Reset the pump fault."""
        self.write_tag("PumpReset", True)

    def is_running(self) -> bool:
        """Return True if the pump is running."""
        return self.read_tag("PumpRunning")

    def has_fault(self) -> bool:
        """Return True if the pump has a fault."""
        return self.read_tag("PumpFault")
