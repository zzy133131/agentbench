"""Abstract base class for agent adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRunResult:
    """Result of running an agent on a single prompt."""

    response: str
    """The agent's text response."""

    duration_ms: float = 0.0
    """Wall-clock time in milliseconds."""

    cost: float = 0.0
    """Estimated cost in USD (if available)."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Extra info (model used, token counts, etc.)."""


class AgentAdapter(ABC):
    """Interface between AgentBench and any agent implementation.

    Implement this class to wrap your agent (whether it is a simple LLM call,
    a complex multi-step agent, or a CLI script) so that AgentBench can
    evaluate it on benchmark tasks.
    """

    name: str = "unnamed"
    """Human-readable identifier for this agent, used in reports."""

    @abstractmethod
    def run(self, prompt: str) -> AgentRunResult:
        """Send a prompt to the agent and return the result."""
