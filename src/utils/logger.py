# test_agent_shield.py
import unittest
from agent import AgentShield

class TestAgentShield(unittest.TestCase):
    def test_optimize_tool_calls(self):
        agent = {'tool_calls': [{'priority': 3}, {'priority': 6}]}
        shield = AgentShield(agent)
        shield.optimize_tool_calls()
        self.assertEqual(len(shield.tool_calls), 1, "Only high-priority calls should remain")

    def test_manage_memory(self):
        agent = {'memory_usage': 50}
        shield = AgentShield(agent)
        shield.manage_memory()
        self.assertEqual(shield.memory_usage, 60, "Memory should increase by 10 (capped at 100)")

    def test_secure_agent(self):
        agent = {'security_level': 'low'}
        shield = AgentShield(agent)
        shield.secure_agent()
        self.assertEqual(agent['security_level'], 'high', "Security level should be upgraded")

if __name__ == '__main__':
    unittest.main()