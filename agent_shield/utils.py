import unittest
from unittest.mock import patch, MagicMock
from orchestrator.tool_call_handler import ToolCallHandler

class TestToolCallHandler(unittest.TestCase):
    @patch('orchestrator.tool_call_handler.make_tool_call')
    def test_tool_call_success(self, mock_make_tool_call):
        mock_make_tool_call.return_value = True
        tool_call_handler = ToolCallHandler()
        self.assertTrue(tool_call_handler.make_tool_call())

    @patch('orchestrator.tool_call_handler.make_tool_call')
    def test_tool_call_failure_with_retries(self, mock_make_tool_call):
        mock_make_tool_call.side_effect = [False, False, True]
        tool_call_handler = ToolCallHandler()
        self.assertTrue(tool_call_handler.make_tool_call())

    @patch('orchestrator.tool_call_handler.make_tool_call')
    def test_tool_call_failure_without_retries(self, mock_make_tool_call):
        mock_make_tool_call.return_value = False
        tool_call_handler = ToolCallHandler()
        self.assertFalse(tool_call_handler.make_tool_call())

    @patch('orchestrator.tool_call_handler.log_error')
    @patch('orchestrator.tool_call_handler.make_tool_call')
    def test_tool_call_error_logging(self, mock_make_tool_call, mock_log_error):
        mock_make_tool_call.side_effect = Exception('Test error')
        tool_call_handler = ToolCallHandler()
        tool_call_handler.make_tool_call()
        mock_log_error.assert_called_once()

if __name__ == '__main__':
    unittest.main()