import threading
import time

class ApiGatekeeper:
    def __init__(self, config: dict):
        self.requests_per_minute = config["requests_per_minute"]
        self.requests_per_hour = config["requests_per_hour"]
        self.max_retries = config["max_retries"]

        self.minute_requests = []
        self.hour_requests = []

        # The thread lock ensures we don't double-count limits during parallel executions
        self.lock = threading.Lock()

    def _cleanup(self):
        now = time.time()

        self.minute_requests = [
            req_time
            for req_time in self.minute_requests
            if now - req_time < 60
        ]

        self.hour_requests = [
            req_time
            for req_time in self.hour_requests
            if now - req_time < 3600
        ]

    def _can_execute(self):
        self._cleanup()

        return (
            len(self.minute_requests) < self.requests_per_minute
            and len(self.hour_requests) < self.requests_per_hour
        )

    def execute(self, func, *args, **kwargs):
        retries = 0

        while retries <= self.max_retries:
            can_run = False
            
            # 1. Lock ONLY to check limits and record timestamps securely
            with self.lock:
                if self._can_execute():
                    current_time = time.time()
                    self.minute_requests.append(current_time)
                    self.hour_requests.append(current_time)
                    can_run = True

            # 2. Execute or Wait OUTSIDE the lock to prevent blocking other agents
            if can_run:
                try:
                    return func(*args, **kwargs)  # Transparently return the API output

                except Exception:
                    retries += 1
                    if retries <= self.max_retries:
                        time.sleep(1)  # Brief wait before retry
            else:
                # Backpressure logic: Sleep briefly and loop again to wait in the "queue"
                time.sleep(2)

        raise RuntimeError(
            "Request failed after maximum retries"
        )