"""Tests for scoring modules."""

from agentbench.scoring.exact_match import ContainsScorer, ExactMatchScorer
from agentbench.tasks.base import BenchmarkTask


class TestExactMatchScorer:
    def setup_method(self) -> None:
        self.scorer = ExactMatchScorer()

    def test_exact_match_pass(self) -> None:
        task = BenchmarkTask(id="t1", name="t1", description="", prompt="?", reference="42")
        result = self.scorer.score(task, "42")
        assert result.passed
        assert result.score == 1.0

    def test_exact_match_case_insensitive(self) -> None:
        task = BenchmarkTask(id="t2", name="t2", description="", prompt="?", reference="Hello")
        result = self.scorer.score(task, "hello")
        assert result.passed

    def test_exact_match_trim(self) -> None:
        task = BenchmarkTask(id="t3", name="t3", description="", prompt="?", reference="yes")
        result = self.scorer.score(task, "  yes  ")
        assert result.passed

    def test_exact_match_fail(self) -> None:
        task = BenchmarkTask(id="t4", name="t4", description="", prompt="?", reference="42")
        result = self.scorer.score(task, "43")
        assert not result.passed
        assert result.score == 0.0


class TestContainsScorer:
    def setup_method(self) -> None:
        self.scorer = ContainsScorer()

    def test_contains_pass(self) -> None:
        task = BenchmarkTask(id="t1", name="t1", description="", prompt="?", reference="fibonacci")
        result = self.scorer.score(task, "def fibonacci(n): return n")
        assert result.passed

    def test_contains_fail(self) -> None:
        task = BenchmarkTask(id="t2", name="t2", description="", prompt="?", reference="binary_search")
        result = self.scorer.score(task, "def linear_search(...)")
        assert not result.passed

    def test_contains_case_insensitive(self) -> None:
        task = BenchmarkTask(id="t3", name="t3", description="", prompt="?", reference="HELLO")
        result = self.scorer.score(task, "say hello world")
        assert result.passed

    def test_contains_strips_markdown(self) -> None:
        task = BenchmarkTask(id="t4", name="t4", description="", prompt="?", reference="print")
        result = self.scorer.score(task, "```python\nprint('hi')\n```")
        assert result.passed
