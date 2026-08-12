import pytest

from plc_test.core.tag_registry import TagRegistry
from plc_test.core.plc_vendor import PLCVendor

from plc_test.simulator.simulated_plc import SimulatedPLC

from plc_test.devices.motor import Motor
from plc_test.devices.pump import Pump
from plc_test.devices.valve import Valve


@pytest.fixture
def tag_registry() -> TagRegistry:
    """Create a fresh tag registry for a test."""

    return TagRegistry()


@pytest.fixture
def plc(tag_registry: TagRegistry) -> SimulatedPLC:
    """Create and connect a simulated PLC."""

    plc = SimulatedPLC(
        tag_registry=tag_registry,
    )

    plc.connect()

    yield plc

    plc.disconnect()


@pytest.fixture
def motor(plc: SimulatedPLC) -> Motor:
    """Create a motor connected to the simulated PLC."""

    return Motor(
        name="TestMotor",
        plc=plc,
    )


@pytest.fixture
def pump(plc: SimulatedPLC) -> Pump:
    """Create a pump connected to the simulated PLC."""

    return Pump(
        name="TestPump",
        plc=plc,
    )


@pytest.fixture
def valve(plc: SimulatedPLC) -> Valve:
    """Create a valve connected to the simulated PLC."""

    return Valve(
        name="TestValve",
        plc=plc,
    )
