"""Task scheduling with project-local helpers."""

import time


def submit(task, run_after_ms):
    return (task, run_after_ms)


def enqueue(task, wait_seconds):
    return submit(task, wait_seconds)  # expect: ORB001


def enqueue_fixed(task, wait_seconds):
    return submit(task, wait_seconds * 1000)


def poll_interval_ms():
    return 200


def loop(iterations):
    for _ in range(iterations):
        time.sleep(poll_interval_ms())  # expect: ORB001


def loop_fixed(iterations):
    for _ in range(iterations):
        time.sleep(poll_interval_ms() / 1000)


def timeout_for(kind, fast_timeout_ms, slow_timeout_seconds):
    return fast_timeout_ms if kind == "fast" else slow_timeout_seconds  # expect: ORB002


def timeout_for_fixed(kind, fast_timeout_ms, slow_timeout_seconds):
    return fast_timeout_ms / 1000 if kind == "fast" else slow_timeout_seconds
