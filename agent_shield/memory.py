"""
In‑memory per‑agent key/value store.
The store lives only for the lifetime of the process – suitable for a demo
or a lightweight SaaS component.  Production would replace this with a
persistent DB (Redis, Postgres, etc.).
"""

from collections import defaultdict
from threading import Lock
from typing import Any, Dict

# ``memory_store`` maps ``agent_id`` → dict of key/value pairs.
memory_store: Dict[str, Dict[str, Any]] = defaultdict(dict)
_store_lock = Lock()


def get_agent_memory(agent_id: str) -> Dict[str, Any]:
    """Return a shallow copy of the memory dict for *agent_id*."""
    with _store_lock:
        return dict(memory_store.get(agent_id, {}))


def set_agent_memory(agent_id: str, key: str, value: Any) -> None:
    """Set ``key`` → ``value`` for *agent_id*."""
    with _store_lock:
        memory_store[agent_id][key] = value


def delete_agent_memory(agent_id: str, key: str) -> bool:
    """Delete *key* from *agent_id* memory. Returns ``True`` if key existed."""
    with _store_lock:
        if key in memory_store.get(agent_id, {}):
            del memory_store[agent_id][key]
            return True
        return False