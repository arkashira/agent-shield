import pytest
from datetime import datetime, timedelta
from agent_shield.security.key_rotation import (
    KeyManager, rotate_keys, get_current_key, get_key_by_version
)

@pytest.fixture
def key_manager(tmp_path):
    # Use a temporary directory for key storage
    return KeyManager(storage_dir=tmp_path)

def test_key_generation(key_manager):
    key = key_manager.generate_key()
    assert len(key) == 32  # 256 bits
    assert isinstance(key, bytes)

def test_key_storage_and_retrieval(key_manager):
    key = key_manager.generate_key()
    key_manager.store_key(key, version=1, timestamp=datetime.utcnow())
    retrieved = key_manager.get_key(1)
    assert retrieved == key

def test_rotation_creates_new_key(key_manager):
    old_key = key_manager.generate_key()
    key_manager.store_key(old_key, version=1, timestamp=datetime.utcnow() - timedelta(days=8))
    rotate_keys(key_manager)
    new_key = key_manager.get_current_key()
    assert new_key != old_key
    assert key_manager.get_current_version() == 2

def test_decryption_with_old_key(key_manager):
    key1 = key_manager.generate_key()
    key_manager.store_key(key1, version=1, timestamp=datetime.utcnow() - timedelta(days=10))
    key2 = key_manager.generate_key()
    key_manager.store_key(key2, version=2, timestamp=datetime.utcnow())
    # Encrypt with key1
    ciphertext = key_manager.encrypt(b"secret", key1)
    # Decrypt with key1
    plaintext = key_manager.decrypt(ciphertext, key1)
    assert plaintext == b"secret"
    # Decrypt with key2 should fail
    with pytest.raises(ValueError):
        key_manager.decrypt(ciphertext, key2)

def test_audit_log_entry(key_manager, caplog):
    rotate_keys(key_manager)
    assert "Rotation completed: version 2" in caplog.text

def test_compliance_endpoint(client, key_manager):
    # Assume Flask/Starlette test client
    response = client.get("/security/compliance")
    assert response.status_code == 200
    data = response.json()
    assert data["current_key_version"] == key_manager.get_current_version()
    assert data["rotation_interval_days"] == 7