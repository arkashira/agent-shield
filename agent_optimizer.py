# agent-shield/agent_shield/core/tool_executor.py

import logging
from typing import Any, Dict
from .exceptions import ToolExecutionError

logger = logging.getLogger(__name__)

class ToolExecutor:
    def __init__(self, tools_registry: Dict[str, Any]):
        self.tools_registry = tools_registry

    def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Executes a tool. Raises ToolExecutionError on failure.
        Previously returned {'status': 'failed:'} on error.
        """
        if tool_name not in self.tools_registry:
            raise ToolExecutionError(f"Tool '{tool_name}' not found", tool_name=tool_name)

        tool_func = self.tools_registry[tool_name]
        
        try:
            # Execute the tool
            result = tool_func(**params)
            return result
        except Exception as e:
            # Log context for debugging (addresses Candidate 1's debugging concern)
            logger.error(f"Tool execution failed: {tool_name}", exc_info=True)
            # Raise structured exception instead of returning 'failed:'
            raise ToolExecutionError(
                message=str(e), 
                tool_name=tool_name, 
                original_error=e
            ) from e