from src.shared.gatekeeper import ApiGatekeeper


def test_execute_success():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 3
    }

    gatekeeper = ApiGatekeeper(config)

    result = gatekeeper.execute(
        lambda: "success"
    )

    assert result == "success"


def test_retry_then_success():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 3
    }

    gatekeeper = ApiGatekeeper(config)

    attempts = {"count": 0}

    def flaky_function():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError("temporary failure")

        return "success"

    result = gatekeeper.execute(
        flaky_function
    )

    assert result == "success"
    assert attempts["count"] == 3


def test_max_retries_exceeded():
    config = {
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "max_retries": 2
    }

    gatekeeper = ApiGatekeeper(config)

    def failing_function():
        raise RuntimeError("always fails")

    import pytest

    with pytest.raises(RuntimeError):
        gatekeeper.execute(
            failing_function
        )