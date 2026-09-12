"""A while-True retry loop around a request with no timeout."""

import time

import requests


def poll(url):
    while True:
        try:
            return requests.get(url)
        except requests.RequestException:
            time.sleep(2)
