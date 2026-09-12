"""Fixture project with deliberate unit mistakes, used by the end-to-end tests."""

import time

DEFAULT_TIMEOUT_MS = 2500


def poll_interval_seconds(base_interval_ms):
    """Wrong: returns milliseconds from a function named for seconds."""
    return base_interval_ms


def wait_for_slot(timeout_ms):
    """Wrong: sleep takes seconds."""
    time.sleep(timeout_ms)


def wait_for_slot_fixed(timeout_ms):
    """Correct: converted before sleeping."""
    time.sleep(timeout_ms / 1000)


def budget_left(elapsed_ms, budget_seconds):
    """Wrong: mixed scales in one subtraction."""
    return budget_seconds - elapsed_ms


def retry_delay(base_delay_ms, attempt):
    """Correct: magnitude arithmetic keeps the unit."""
    return base_delay_ms * 2**attempt
