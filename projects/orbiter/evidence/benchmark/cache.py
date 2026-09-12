"""Cache expiry handling."""

import time


def is_expired(stored_at_seconds, ttl_ms):
    age_seconds = time.monotonic() - stored_at_seconds
    return age_seconds > ttl_ms  # expect: ORB002


def is_expired_fixed(stored_at_seconds, ttl_ms):
    age_seconds = time.monotonic() - stored_at_seconds
    return age_seconds > ttl_ms / 1000


def ttl_seconds(configured_ttl_ms):
    return configured_ttl_ms  # expect: ORB004


def ttl_seconds_fixed(configured_ttl_ms):
    return configured_ttl_ms / 1000


def refresh_after_minutes(interval_seconds):
    interval_minutes = interval_seconds  # expect: ORB003
    return interval_minutes


def refresh_after_minutes_fixed(interval_seconds):
    interval_minutes = interval_seconds / 60
    return interval_minutes
