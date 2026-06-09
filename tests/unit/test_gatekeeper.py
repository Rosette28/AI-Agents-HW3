from unittest.mock import patch

import pytest

from src.shared.gatekeeper import ApiGatekeeper


def test_execute_success():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 3,
    }

    gatekeeper = ApiGatekeeper(config)

    result = gatekeeper.execute(
        lambda: "success",
    )

    assert result == "success"


def test_retry_then_success():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 3,
    }

    gatekeeper = ApiGatekeeper(config)

    attempts = {"count": 0}

    def flaky_function():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError("temporary failure")

        return "success"

    result = gatekeeper.execute(
        flaky_function,
    )

    assert result == "success"
    assert attempts["count"] == 3


def test_max_retries_exceeded():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 2,
    }

    gatekeeper = ApiGatekeeper(config)

    def failing_function():
        raise RuntimeError("always fails")


    with pytest.raises(RuntimeError):
        gatekeeper.execute(
            failing_function,
        )


@patch("time.sleep") # Mock sleep so the test doesn't actually wait for 2 seconds
def test_rate_limit_backpressure(mock_sleep):
    config = {
        "requests_per_minute": 2, # Tight limit
        "requests_per_hour": 100,
        "max_retries": 3,
    }
    gatekeeper = ApiGatekeeper(config)

    # Fire 2 successful requests (hits the limit)
    gatekeeper.execute(lambda: "success 1")
    gatekeeper.execute(lambda: "success 2")

    # The 3rd request should trigger backpressure (time.sleep)
    gatekeeper.execute(lambda: "success 3")

    # Assert that the gatekeeper forced a sleep due to rate limits
    mock_sleep.assert_called()
