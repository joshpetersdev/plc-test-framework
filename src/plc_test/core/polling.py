import time
from typing import Any, Callable

from .exceptions import PollingTimeoutError


def wait_until(
    condition: Callable[[], bool],
    timeout: float,
    interval: float = 0.1,
    description: str = "condition",
) -> None:
    """
    Wait until a condition becomes True.

    Args:
        condition: Callable that returns True when the desired condition
            has been satisfied.
        timeout: Maximum amount of time to wait, in seconds.
        interval: Time between condition checks, in seconds.
        description: Human-readable description of the condition.

    Raises:
        PollingTimeoutError: If the condition is not satisfied before
            the timeout expires.
        ValueError: If timeout or interval is invalid.
    """

    if timeout <= 0:
        raise ValueError("timeout must be greater than zero.")

    if interval <= 0:
        raise ValueError("interval must be greater than zero.")

    start_time = time.monotonic()

    while True:
        if condition():
            return

        elapsed_time = time.monotonic() - start_time

        if elapsed_time >= timeout:
            raise PollingTimeoutError(
                f"Timed out waiting for {description} "
                f"after {timeout:.2f} seconds."
            )

        time.sleep(interval)
