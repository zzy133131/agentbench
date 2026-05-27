"""Agent adapters for connecting different agent implementations to the benchmark runner."""

from agentbench.adapter.base import AgentAdapter
from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.adapter.subprocess_adapter import SubprocessAdapter

__all__ = ["AgentAdapter", "FunctionAdapter", "SubprocessAdapter"]
