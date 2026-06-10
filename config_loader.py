import os
import yaml
from unittest.mock import patch
from agent_shield.config_loader import ConfigLoader

def test_load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
    loader = ConfigLoader()
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    loaded_config = loader.load_config()
    assert loaded_config == config

def test_log_shield_activation():
    import logging
    with patch('agent_shield.config_loader.logging.Logger.info') as mock_log:
        ConfigLoader().load_config()
        mock_log.assert_called_once_with("Agent Shield activated.")

def test_no_config_error():
    with patch('os.path.isfile', return_value=False):
        with pytest.raises(FileNotFoundError):
            ConfigLoader().load_config()

def test_invalid_config_error():
    config_path = os.path.join(os.path.dirname(__file__), 'invalid_config.yaml')
    with patch('os.path.isfile', return_value=True):
        with pytest.raises(YAMLError):
            ConfigLoader().load_config(config_path)