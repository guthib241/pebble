"""Geographic and angular helpers."""

import math


def bearing_component(heading_deg):
    return math.cos(heading_deg)  # expect: ORB001


def bearing_component_fixed(heading_deg):
    return math.cos(math.radians(heading_deg))


def slope(rise_meters, run_km):
    return rise_meters / run_km + 0.0


def total_distance_meters(leg_one_meters, leg_two_km):
    return leg_one_meters + leg_two_km  # expect: ORB002


def total_distance_meters_fixed(leg_one_meters, leg_two_km):
    return leg_one_meters + leg_two_km * 1000


def turn_rate_rad(delta_deg, elapsed_seconds):
    # known-miss: ORB003 - dividing one dimension by another produces a rate
    # (degrees per second), and rates are outside the unit model.
    rate_rad = delta_deg / elapsed_seconds
    return rate_rad


def turn_rate_rad_fixed(delta_deg, elapsed_seconds):
    rate_rad = math.radians(delta_deg) / elapsed_seconds
    return rate_rad
