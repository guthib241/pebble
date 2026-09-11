"""An asyncio deadline that is shorter than the retries beneath it."""

import asyncio

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(4), wait=wait_fixed(2))
async def call_upstream():
    return httpx.get("https://example.invalid/data", timeout=5)


async def handler():
    return await asyncio.wait_for(call_upstream(), timeout=5)
