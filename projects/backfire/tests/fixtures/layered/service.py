"""Middle layer: a hand-rolled retry loop around the client."""

import time

from client import ApiClient


class UserService:
    def __init__(self):
        self.client = ApiClient()

    def fetch(self, user_id):
        for attempt in range(2):
            try:
                return self.client.get_user(user_id)
            except OSError:
                time.sleep(1)
        raise RuntimeError("give up")
