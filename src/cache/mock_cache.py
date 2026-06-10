class MockCache:
    def __init__(self):
        self.mock_data = {
            "tool_1": {"status": "success", "data": "mocked response"},
            "tool_2": {"status": "success", "data": "another mocked response"}
        }

    def get_mock_data(self, tool_name):
        return self.mock_data.get(tool_name, {"status": "failure", "data": "no mock data available"})