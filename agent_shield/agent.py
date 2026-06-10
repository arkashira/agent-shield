from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
import subprocess


@dataclass
class Interaction:
    """Simple record of a single agent interaction."""
    query: str
    tool: str
    output: str


class InteractionLog:
    """In-memory log of all interactions."""
    def __init__(self) -> None:
        self._entries: List[Interaction] = []

    def add(self, interaction: Interaction) -> None:
        self._entries.append(interaction)

    def all(self) -> List[Interaction]:
        return list(self._entries)


class AgentShield:
    """
    Minimal implementation of the AgentShield feature.
    It forwards the user query to a mock tool (``echo``) and records the interaction.
    """

    def __init__(self, log: InteractionLog | None = None) -> None:
        self.log = log or InteractionLog()

    def _call_tool(self, tool: str, query: str) -> str:
        """
        Execute a simple shell tool and return its stdout.
        For safety in tests we only allow ``echo``.
        """
        if tool != "echo":
            raise ValueError(f"Unsupported tool: {tool}")
        result = subprocess.run([tool, query], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def process(self, query: str, tool: str = "echo") -> str:
        """
        Process a user query by delegating to the specified tool.
        The interaction is logged and the tool output is returned.
        """
        output = self._call_tool(tool, query)
        self.log.add(Interaction(query=query, tool=tool, output=output))
        return output


__all__ = ["AgentShield", "InteractionLog", "Interaction"]