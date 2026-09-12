"""A single bounded retry with backoff and an explicit timeout."""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=2))
def load_profile(user_id):
    client = httpx.Client(timeout=2.0)
    return client.get(f"https://example.invalid/users/{user_id}")


def main():
    return load_profile(7)
