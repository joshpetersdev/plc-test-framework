from typing import Any

from plc_test.core.exceptions import TagNotFoundError
from plc_test.core.plc_interface import PLCInterface
from plc_test.core.plc_vendor import PLCVendor
from plc_test.core.tag import Tag, TagAccess, TagDataType
from plc_test.core.tag_registry import TagRegistry

from .tag_mapping import SimulatedTagMapping


class SimulatedPLC(PLCInterface):
    """In-memory PLC simulator for functional testing."""

    def __init__(self, tag_registry: TagRegistry) -> None:
        super().__init__(tag_registry)

        self._connected = False
        self._values: dict[str, Any] = {}

        self._initialize_tags()

    def _initialize_tags(self) -> None:
        """Create the tags used by the simulated devices."""

        self._register_bool_tag(
            "MotorStart",
            "motor.start",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "MotorStop",
            "motor.stop",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "MotorRunning",
            "motor.running",
            TagAccess.READ_ONLY,
        )

        self._register_bool_tag(
            "MotorFault",
            "motor.fault",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "MotorReset",
            "motor.reset",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "PumpStart",
            "pump.start",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "PumpStop",
            "pump.stop",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "PumpRunning",
            "pump.running",
            TagAccess.READ_ONLY,
        )

        self._register_bool_tag(
            "PumpFault",
            "pump.fault",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "PumpReset",
            "pump.reset",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "ValveOpen",
            "valve.open",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "ValveClose",
            "valve.close",
            TagAccess.READ_WRITE,
        )

        self._register_bool_tag(
            "ValveOpenFeedback",
            "valve.open_feedback",
            TagAccess.READ_ONLY,
        )

        self._register_bool_tag(
            "ValveClosedFeedback",
            "valve.closed_feedback",
            TagAccess.READ_ONLY,
            initial_value=True,
        )

        self._register_bool_tag(
            "ValveFault",
            "valve.fault",
            TagAccess.READ_WRITE,
        )

    def _register_bool_tag(
        self,
        name: str,
        identifier: str,
        access: TagAccess,
        initial_value: bool = False,
    ) -> None:
        """Register a BOOL tag and its simulator mapping."""

        tag = Tag(
            name=name,
            data_type=TagDataType.BOOL,
            access=access,
        )

        mapping = SimulatedTagMapping(
            tag=tag,
            identifier=identifier,
        )

        self.tag_registry.register_tag(tag)

        self.tag_registry.register_mapping(
            tag_name=name,
            vendor=PLCVendor.SIMULATOR,
            mapping=mapping,
        )

        self._values[name] = initial_value

    def connect(self) -> None:
        """Connect to the simulated PLC."""

        self._connected = True

    def disconnect(self) -> None:
        """Disconnect from the simulated PLC."""

        self._connected = False

    def is_connected(self) -> bool:
        """Return True if the simulator is connected."""

        return self._connected

    def read_tag(self, tag_name: str) -> Any:
        """Read a value from the simulated PLC."""

        self._ensure_connected()

        if not self.tag_registry.contains(tag_name):
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            )

        return self._values[tag_name]

    def write_tag(
        self,
        tag_name: str,
        value: Any,
    ) -> None:
        """Write a value to the simulated PLC."""

        self._ensure_connected()

        if not self.tag_registry.contains(tag_name):
            raise TagNotFoundError(
                f"Tag '{tag_name}' is not registered."
            )

        tag = self.tag_registry.get_tag(tag_name)

        self._validate_value(tag, value)

        self._values[tag_name] = value

        self._execute_plc_logic(tag_name)

    def _execute_plc_logic(self, tag_name: str) -> None:
        """Execute simulated PLC logic after a tag write."""

        if tag_name == "MotorStart":
            if self._values["MotorStart"]:
                self._values["MotorRunning"] = True

                self._values["MotorStart"] = False

        elif tag_name == "MotorStop":
            if self._values["MotorStop"]:
                self._values["MotorRunning"] = False

                self._values["MotorStop"] = False

        elif tag_name == "MotorReset":
            if self._values["MotorReset"]:
                self._values["MotorFault"] = False
                self._values["MotorReset"] = False

        elif tag_name == "PumpStart":
            if self._values["PumpStart"]:
                self._values["PumpRunning"] = True

                self._values["PumpStart"] = False

        elif tag_name == "PumpStop":
            if self._values["PumpStop"]:
                self._values["PumpRunning"] = False

                self._values["PumpStop"] = False

        elif tag_name == "PumpReset":
            if self._values["PumpReset"]:
                self._values["PumpFault"] = False
                self._values["PumpReset"] = False

        elif tag_name == "ValveOpen":
            if self._values["ValveOpen"]:
                self._values["ValveOpenFeedback"] = True
                self._values["ValveClosedFeedback"] = False

                self._values["ValveOpen"] = False

        elif tag_name == "ValveClose":
            if self._values["ValveClose"]:
                self._values["ValveOpenFeedback"] = False
                self._values["ValveClosedFeedback"] = True

                self._values["ValveClose"] = False

    def _validate_value(
        self,
        tag: Tag,
        value: Any,
    ) -> None:
        """Validate a value against the tag's data type."""

        if tag.data_type == TagDataType.BOOL:
            if not isinstance(value, bool):
                raise TypeError(
                    f"Tag '{tag.name}' expects a bool, "
                    f"got {type(value).__name__}."
                )

    def _ensure_connected(self) -> None:
        """Raise an error if the simulator is disconnected."""

        if not self._connected:
            raise ConnectionError(
                "Simulated PLC is not connected."
            )
