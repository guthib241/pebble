"""HTTP client configuration. Mixed correct and incorrect unit handling."""

import requests
import socket
import time

CONNECT_TIMEOUT_MS = 2500
MS_PER_SECOND = 1000


def fetch(url, read_timeout_ms):
    return requests.get(url, timeout=read_timeout_ms)  # expect: ORB001


def fetch_fixed(url, read_timeout_ms):
    return requests.get(url, timeout=read_timeout_ms / MS_PER_SECOND)


def open_socket(host, port, connect_timeout_ms):
    sock = socket.create_connection((host, port))
    sock.settimeout(connect_timeout_ms)  # expect: ORB001
    return sock


def open_socket_fixed(host, port, connect_timeout_ms):
    sock = socket.create_connection((host, port))
    sock.settimeout(connect_timeout_ms / 1000)
    return sock


def backoff(attempt, base_delay_ms):
    delay_ms = base_delay_ms * 2**attempt
    time.sleep(delay_ms)  # expect: ORB001
    return delay_ms


def backoff_fixed(attempt, base_delay_ms):
    delay_ms = base_delay_ms * 2**attempt
    time.sleep(delay_ms / 1000)
    return delay_ms


def deadline_seconds(budget_ms):
    return time.monotonic() + budget_ms  # expect: ORB002


def deadline_seconds_fixed(budget_ms):
    return time.monotonic() + budget_ms / 1000
