import pytest
from unittest.mock import patch, MagicMock
from agent_shield.logs.error_classifier import (
    classify_error,
    retry_tool_call,
    _backoff_interval,
)

# ---------- classify_error ----------
@pytest.mark.parametrize(
    "exception,expected_category",
    [
        (MagicMock(spec=RateLimitError), "RATE_LIMIT"),
        (MagicMock(spec=NetworkError), "NETWORK"),
        (MagicMock(), "UNKNOWN"),
    ],
)
def test_classify_error_returns_expected_category(exception, expected_category):
    assert classify_error(exception) == expected_category


# ---------- _backoff_interval ----------
@pytest.mark.parametrize(
    "attempt,expected_interval_ms",
    [
        (1, 500),
        (2, 1000),
        (3, 2000),
    ],
)
def test_backoff_interval(attempt, expected_interval_ms):
    assert _backoff_interval(attempt) == expected_interval_ms


# ---------- retry_tool_call ----------
@patch("agent_shield.logs.error_classifier.time.sleep")
@patch("agent_shield.logs.error_classifier.logger")
def test_retry_tool_call_success_on_second_attempt(mock_logger, mock_sleep):
    tool = MagicMock()
    tool.call.side_effect = [Exception("Rate limit"), MagicMock(return_value="ok")]

    result = retry_tool_call(tool, "tool_name")

    assert result == "ok"
    assert tool.call.call_count == 2
    # Verify logging on failure
    mock_logger.error.assert_called_once()
    log_args = mock_logger.error.call_args[0][0]
    assert "RATE_LIMIT" in log_args
    assert "Attempt 1" in log_args
    # Verify back‑off sleep called once with 500ms
    mock_sleep.assert_called_once_with(0.5)


@patch("agent_shield.logs.error_classifier.time.sleep")
@patch("agent_shield.logs.error_classifier.logger")
def test_retry_tool_call_exhausts_attempts(mock_logger, mock_sleep):
    tool = MagicMock()
    tool.call.side_effect = Exception("Network")

    with pytest.raises(Exception):
        retry_tool_call(tool, "tool_name")

    assert tool.call.call_count == 3
    # 3 error logs (attempts 1‑3)
    assert mock_logger.error.call_count == 3
    # Sleep called twice (after attempts 1 & 2)
    assert mock_sleep.call_count == 2
    # Verify final log contains UNKNOWN if classification fails
    last_log = mock_logger.error.call_args_list[-1][0][0]
    assert "NETWORK" in last_log