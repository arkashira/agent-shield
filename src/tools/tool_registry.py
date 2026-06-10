import time
from .cache.mock_cache import MockCache
from .utils.logger import Logger

logger = Logger()
mock_cache = MockCache()

class ToolRegistry:
    def __init__(self):
        self.circuit_breaker_open = False
        self.consecutive_failures = 0

    def execute_tool(self, tool_name, *args, **kwargs):
        if self.circuit_breaker_open:
            logger.log(f"{time.time()} - Circuit breaker is open, using fallback.")
            return mock_cache.get_mock_data(tool_name)

        try:
            result = self._call_tool(tool_name, *args, **kwargs)
            self.consecutive_failures = 0
            return result
        except Exception as e:
            self.consecutive_failures += 1
            logger.log(f"{time.time()} - Tool call failed: {str(e)}")
            if self.consecutive_failures >= 5:
                self.circuit_breaker_open = True
                logger.log(f"{time.time()} - Circuit breaker tripped due to 5 consecutive failures.")
                time.sleep(30)
                self.circuit_breaker_open = False
                self.consecutive_failures = 0
            else:
                # Exponential backoff logic
                wait_time = min((2 ** (self.consecutive_failures - 1)), 4)
                logger.log(f"{time.time()} - Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
                return self.execute_tool(tool_name, *args, **kwargs)

    def _call_tool(self, tool_name, *args, **kwargs):
        # Simulate tool call
        if tool_name == "tool_with_transient_error":
            raise Exception("Transient error occurred")
        return {"status": "success", "data": f"Response from {tool_name}"}