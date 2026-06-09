"""API Gatekeeper module for rate limiting and backpressure."""
import threading
import time
from collections.abc import Callable
from typing import Any


class ApiGatekeeper:
    """Centralized API call manager."""

    def __init__(self, config: dict) -> None:
        """Initialize the gatekeeper with rate limits."""
        self.requests_per_minute = config["requests_per_minute"]
        self.requests_per_hour = config["requests_per_hour"]
        self.max_retries = config.get("max_retries", 3)

        self.minute_requests: list[float] = []
        self.hour_requests: list[float] = []
        self.lock = threading.Lock()

        self.minute_window = 60
        self.hour_window = 3600

    def _cleanup(self) -> None:
        """Remove old requests from the tracking lists."""
        now = time.time()
        self.minute_requests = [
            req_time
            for req_time in self.minute_requests
            if now - req_time < self.minute_window
        ]
        self.hour_requests = [
            req_time
            for req_time in self.hour_requests
            if now - req_time < self.hour_window
        ]

    def _can_execute(self) -> bool:
        """Check if a request can be executed right now."""
        self._cleanup()
        return (len(self.minute_requests) < self.requests_per_minute and
                len(self.hour_requests) < self.requests_per_hour)

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any: # noqa: ANN401
        """Execute a function while respecting rate limits, with retries."""
        retries = 0
        while True:
            with self.lock:
                if self._can_execute():
                    self.minute_requests.append(time.time())
                    self.hour_requests.append(time.time())

                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        retries += 1
                        if retries <= self.max_retries:
                            time.sleep(2)
                            continue
                        msg = "Request failed after maximum retries"
                        raise RuntimeError(msg) from e

            time.sleep(2)
