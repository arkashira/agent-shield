# tests/test_security.py
import pytest
from agent_shield.security import is_call_safe

def test_whitelisted_tool():
    ok, _ = is_call_safe({"name": "search", "arguments": {"q": "foo"}})
    asse
