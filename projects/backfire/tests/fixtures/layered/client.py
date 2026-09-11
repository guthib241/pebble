"""Bottom layer: a requests session with transport-level retries."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(total=4, backoff_factor=0.5))
        self.session.mount("https://", adapter)

    def get_user(self, user_id):
        return self.session.get(f"https://example.invalid/users/{user_id}", timeout=5)
