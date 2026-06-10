import unittest
from unittest.mock import patch
from agent_shield.metrics.memory_metrics import MemoryMetrics

class TestMemoryMetrics(unittest.TestCase):
    @patch('agent_shield.metrics.memory_metrics.psutil')
    def test_get_memory_metrics(self, mock_psutil):
        mock_psutil.virtual_memory.return_value = psutil.VirtualMemory(percent=50, total=1000000, used=500000)
        memory_metrics = MemoryMetrics()
        memory_data = memory_metrics.get_memory_metrics()
        self.assertIn('memory_used', memory_data)
        self.assertIn('memory_total', memory_data)
        self.assertIn('memory_percent', memory_data)

    @patch('agent_shield.metrics.memory_metrics.time')
    def test_update_memory_metrics(self, mock_time):
        memory_metrics = MemoryMetrics()
        memory_metrics.update_memory_metrics()
        mock_time.sleep.assert_called_once_with(300)  # 5 minutes in seconds

    # Add more tests for other methods in MemoryMetrics class as needed