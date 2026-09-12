"""Fixture project: byte sizes and percentages."""


def progress_pct(sent_bytes, total_bytes):
    """Wrong: a fraction assigned to a percent name."""
    used_pct = sent_bytes / total_bytes
    return used_pct


def progress_pct_fixed(sent_bytes, total_bytes):
    """Correct."""
    used_pct = sent_bytes / total_bytes * 100
    return used_pct


def chunk_budget(limit_mb):
    """Wrong: a megabyte count used where bytes are expected."""
    return bytearray(limit_mb)
