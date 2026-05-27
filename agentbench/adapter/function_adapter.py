"""Adapter that wraps any callable (function, lambda, or object with ``__call__``)."""

import time
from typing import Any, Callable

from agentbench.adapter.base import AgentAdapter, AgentRunResult


class FunctionAdapter(AgentAdapter):
    """Wraps a Python function as an agent for benchmarking.

    Useful for testing simple agents, prompts, or chain-of-thought
    pipelines defined as functions.

    Args:
        fn: A callable that accepts a prompt string and returns a response string.
        name: Optional name for the adapter (defaults to the function's ``__name__``).
    """

    def __init__(self, fn: Callable[[str], str], name: str | None = None) -> None:
        self._fn = fn
        self.name = name or getattr(fn, "__name__", "unnamed")

    def run(self, prompt: str) -> AgentRunResult:
        start = time.perf_counter()
        try:
            response = self._fn(prompt)
            duration = (time.perf_counter() - start) * 1000
            return AgentRunResult(response=response, duration_ms=round(duration, 1))
        except Exception as exc:
            duration = (time.perf_counter() - start) * 1000
            return AgentRunResult(
                response=f"Error: {exc}",
                duration_ms=round(duration, 1),
                metadata={"error": str(exc)},
            )
