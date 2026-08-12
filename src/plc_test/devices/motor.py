from plc_test.core.device import Device


class Motor(Device):
    """Represents a PLC-controlled motor."""

    def start(self) -> None:
        """Command the motor to start."""
        self.write_tag("MotorStart", True)

    def stop(self) -> None:
        """Command the motor to stop."""
        self.write_tag("MotorStop", True)

    def reset(self) -> None:
        """Reset the motor fault."""
        self.write_tag("MotorReset", True)

    def is_running(self) -> bool:
        """Return True if the motor is running."""
        return self.read_tag("MotorRunning")

    def has_fault(self) -> bool:
        """Return True if the motor has a fault."""
        return self.read_tag("MotorFault")
