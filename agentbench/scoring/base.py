"""Base class for all scoring strategies."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from agentbench.tasks.base import BenchmarkTask


@dataclass
class ScoreResult:
    """Result of scoring a single task response."""

    score: float
    """Normalised score (0.0 to task.max_score)."""

    max_score: float
    """Maximum possible score."""

    passed: bool
    """Whether the score meets the passing threshold."""

    details: str = ""
    """Explanation of the scoring decision, or error message."""

    metadata: dict[str, Any] | None = None
    """Optional extra scoring data."""

    @property
    def percentage(self) -> float:
        """Score as a percentage (0-100)."""
        if self.max_score <= 0:
            return 0.0
        return (self.score / self.max_score) * 100


class Scorer(ABC):
    """Abstract scorer that evaluates an agent's response against a task."""

    @abstractmethod
    def score(self, task: BenchmarkTask, response: str) -> ScoreResult:
        """Evaluate *response* against *task* and return a ScoreResult."""
