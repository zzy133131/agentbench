"""Exact-match and substring-containment scorers."""

import re

from agentbench.scoring.base import Scorer, ScoreResult
from agentbench.tasks.base import BenchmarkTask


class ExactMatchScorer(Scorer):
    """A response passes if it matches the reference answer.

    Comparison is case-insensitive and ignores leading/trailing whitespace.
    """

    def score(self, task: BenchmarkTask, response: str) -> ScoreResult:
        expected = task.reference.strip().lower()
        actual = response.strip().lower()

        passed = expected == actual
        return ScoreResult(
            score=task.max_score if passed else 0.0,
            max_score=task.max_score,
            passed=passed,
            details="Exact match" if passed else f"Expected '{task.reference}', got '{response.strip()[:100]}'",
        )


class ContainsScorer(Scorer):
    """A response passes if the reference string appears within it.

    Comparison is case-insensitive.
    """

    def __init__(self, strip_markdown: bool = True) -> None:
        self.strip_markdown = strip_markdown

    def score(self, task: BenchmarkTask, response: str) -> ScoreResult:
        text = response.strip()
        if self.strip_markdown:
            # Strip common markdown fences for cleaner matching
            text = re.sub(r"```\w*\n?", "", text)

        expected = task.reference.strip().lower()
        passed = expected in text.lower()

        return ScoreResult(
            score=task.max_score if passed else 0.0,
            max_score=task.max_score,
            passed=passed,
            details="Contains expected text" if passed else f"Expected to contain '{task.reference}'",
        )
