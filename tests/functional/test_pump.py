from plc_test.devices.pump import Pump


class TestPump:
    """Functional tests for the Pump device."""

    def test_pump_starts(self, pump: Pump) -> None:
        """Verify that starting the pump causes it to run."""

        pump.start()

        assert pump.is_running() is True

    def test_pump_stops(self, pump: Pump) -> None:
        """Verify that stopping the pump causes it to stop."""

        pump.start()
        assert pump.is_running() is True

        pump.stop()

        assert pump.is_running() is False

    def test_pump_reset(self, pump: Pump) -> None:
        """Verify that a pump fault can be reset."""

        pump.start()

        pump.write_tag("PumpFault", True)

        assert pump.has_fault() is True

        pump.reset()

        assert pump.has_fault() is False

    def test_pump_initial_state(self, pump: Pump) -> None:
        """Verify the pump starts stopped and fault-free."""

        assert pump.is_running() is False
        assert pump.has_fault() is False
