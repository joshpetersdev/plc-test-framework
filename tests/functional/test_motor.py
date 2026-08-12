import pytest

from plc_test.devices.motor import Motor


class TestMotor:
    """Functional tests for the Motor device."""

    def test_motor_starts(self, motor: Motor) -> None:
        """Verify that starting the motor causes it to run."""

        motor.start()

        assert motor.is_running() is True

    def test_motor_stops(self, motor: Motor) -> None:
        """Verify that stopping the motor causes it to stop."""

        motor.start()
        assert motor.is_running() is True

        motor.stop()

        assert motor.is_running() is False

    def test_motor_reset(self, motor: Motor) -> None:
        """Verify that a motor fault can be reset."""

        motor.start()

        # Simulate a fault condition.
        motor.write_tag("MotorFault", True)

        assert motor.has_fault() is True

        motor.reset()

        assert motor.has_fault() is False

    def test_motor_initial_state(self, motor: Motor) -> None:
        """Verify the motor starts in a stopped, fault-free state."""

        assert motor.is_running() is False
        assert motor.has_fault() is False
