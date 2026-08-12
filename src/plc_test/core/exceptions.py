class PLCFrameworkError(Exception):
    """Base exception for all PLC test framework errors."""


class PLCConnectionError(PLCFrameworkError):
    """Raised when a connection to the PLC cannot be established."""


class PLCCommunicationError(PLCFrameworkError):
    """Raised when communication with the PLC fails."""


class PLCReadError(PLCCommunicationError):
    """Raised when reading a PLC tag fails."""


class PLCWriteError(PLCCommunicationError):
    """Raised when writing to a PLC tag fails."""


class TagError(PLCFrameworkError):
    """Base exception for tag-related errors."""


class TagNotFoundError(TagError):
    """Raised when a requested tag does not exist."""


class TagReadOnlyError(TagError):
    """Raised when attempting to write to a read-only tag."""


class TagWriteOnlyError(TagError):
    """Raised when attempting to read from a write-only tag."""


class TagTypeError(TagError):
    """Raised when a value has an incompatible type for a tag."""


class PollingError(PLCFrameworkError):
    """Base exception for polling-related errors."""


class PollingTimeoutError(PollingError):
    """Raised when a polling condition is not satisfied before timeout."""
