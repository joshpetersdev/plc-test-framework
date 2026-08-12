from plc_test.devices.valve import Valve


class TestValve:
    """Functional tests for the Valve device."""

    def test_valve_opens(self, valve: Valve) -> None:
        """Verify that opening the valve results in open feedback."""

        valve.open()

        assert valve.is_open() is True
        assert valve.is_closed() is False

    def test_valve_closes(self, valve: Valve) -> None:
        """Verify that closing the valve results in closed feedback."""

        valve.open()

        assert valve.is_open() is True

        valve.close()

        assert valve.is_open() is False
        assert valve.is_closed() is True

    def test_valve_initial_state(self, valve: Valve) -> None:
        """Verify the valve starts closed."""

        assert valve.is_open() is False
        assert valve.is_closed() is True

    def test_valve_has_no_fault(self, valve: Valve) -> None:
        """Verify the valve starts without a fault."""

        assert valve.has_fault() is False
