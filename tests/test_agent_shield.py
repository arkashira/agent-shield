import yaml
import os
import unittest

class TestAgentShieldConfig(unittest.TestCase):
    def test_yaml_syntax(self):
        with open('/opt/axentx/agent-shield/agent-shield.yaml', 'r') as file:
            try:
                yaml.safe_load(file)
            except yaml.YAMLError as e:
                self.fail(f"Invalid YAML syntax: {e}")

    def test_config_loading(self):
        # Mock the config directory and file
        config_dir = '/opt/axentx/agent-shield/'
        config_file = 'agent-shield.yaml'
        # Load the config
        loaded_config = load_config(os.path.join(config_dir, config_file))
        self.assertIsNotNone(loaded_config)

    def test_shield_activation_logging(self):
        # Mock the logging mechanism
        log_message = log_shield_activation()
        self.assertIn("Shield activated", log_message)

if __name__ == '__main__':
    unittest.main()