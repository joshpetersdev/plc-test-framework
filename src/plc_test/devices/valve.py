from plc_test.core.device import Device


class Valve(Device):
    """Represents a PLC-controlled valve."""

    def open(self) -> None:
        """Command the valve to open."""
        self.write_tag("ValveOpen", True)

    def close(self) -> None:
        """Command the valve to close."""
        self.write_tag("ValveClose", True)

    def is_open(self) -> bool:
        """Return True if the valve is open."""
        return self.read_tag("ValveOpenFeedback")

    def is_closed(self) -> bool:
        """Return True if the valve is closed."""
        return self.read_tag("ValveClosedFeedback")

    def has_fault(self) -> bool:
        """Return True if the valve has a fault."""
        return self.read_tag("ValveFault")
