"""Top layer: an HTTP handler that retries the service call."""

from tenacity import retry, stop_after_attempt, wait_fixed

from service import UserService


@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def handle_request(user_id):
    service = UserService()
    return service.fetch(user_id)
