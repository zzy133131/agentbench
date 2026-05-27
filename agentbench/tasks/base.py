"""Core data structures for benchmark tasks."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ScoringMethod(str, Enum):
    """Supported scoring strategies for evaluating agent responses."""

    EXACT_MATCH = "exact_match"
    """Response must match the reference exactly (case-insensitive, stripped)."""

    CONTAINS = "contains"
    """Reference string must appear somewhere in the response."""

    LLM_JUDGE = "llm_judge"
    """An LLM evaluates response quality against a rubric."""


@dataclass
class BenchmarkTask:
    """A single evaluation task for an AI agent.

    Each task has a prompt that is sent to the agent, a reference answer,
    and a scoring method used to evaluate the response.
    """

    id: str
    """Unique identifier (e.g. ``"math-001"``)."""

    name: str
    """Human-readable short name."""

    description: str
    """Explanation of what the task measures."""

    prompt: str
    """The prompt sent to the agent."""

    reference: str = ""
    """Expected answer (used by exact_match / contains scorers)."""

    scoring: ScoringMethod = ScoringMethod.EXACT_MATCH
    """Scoring method to evaluate the response."""

    rubric: str = ""
    """Evaluation criteria (required for LLM_JUDGE scoring)."""

    tags: list[str] = field(default_factory=list)
    """Tags for filtering and categorising tasks (e.g. ``"math"``, ``"reasoning"``)."""

    max_score: float = 1.0
    """Maximum possible score for this task."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Optional extra data (difficulty, source, etc.)."""
