"""Disk accounting."""

import os


def free_space_ok(path, required_mb):
    stat = os.stat(path)
    return stat.st_size > required_mb  # expect: ORB002


def free_space_ok_fixed(path, required_mb):
    stat = os.stat(path)
    return stat.st_size > required_mb * 1000000


def allocate(buffer_kb):
    return bytearray(buffer_kb)  # expect: ORB001


def allocate_fixed(buffer_kb):
    return bytearray(buffer_kb * 1024)


def quota_bytes(limit_gb):
    return limit_gb  # expect: ORB004


def quota_bytes_fixed(limit_gb):
    return limit_gb * 1000000000


def chunk_total(header_bytes, payload_kb):
    return header_bytes + payload_kb  # expect: ORB002


def chunk_total_fixed(header_bytes, payload_kb):
    return header_bytes + payload_kb * 1000
