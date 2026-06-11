"""Integration tests for the SDK."""
from src.sdk.sdk import CrewPipelineSDK


def test_sdk_creation() -> None:
    """Test that the SDK initializes agents correctly."""
    sdk = CrewPipelineSDK()

    assert sdk.researcher is not None
    assert sdk.writer is not None
    assert sdk.editor is not None
