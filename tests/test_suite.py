"""Tests for BenchmarkSuite."""

from agentbench.suite import BenchmarkSuite
from agentbench.tasks.base import BenchmarkTask


class TestBenchmarkSuite:
    def test_empty_suite(self) -> None:
        suite = BenchmarkSuite(name="empty")
        assert len(suite) == 0
        assert suite.name == "empty"

    def test_all_builtins(self) -> None:
        suite = BenchmarkSuite.all_builtins()
        assert len(suite) > 30  # all built-in tasks

    def test_by_tag(self) -> None:
        suite = BenchmarkSuite.by_tag("math")
        assert len(suite) >= 10
        for t in suite.tasks:
            assert "math" in t.tags

    def test_by_tags_any(self) -> None:
        suite = BenchmarkSuite.by_tags(["math", "coding"], mode="any")
        task_ids = {t.id for t in suite.tasks}
        assert any("math-" in tid for tid in task_ids)
        assert any("code-" in tid for tid in task_ids)

    def test_by_ids(self) -> None:
        suite = BenchmarkSuite.by_ids(["math-001", "reason-001"])
        assert len(suite) == 2
        assert suite.tasks[0].id == "math-001"
        assert suite.tasks[1].id == "reason-001"

    def test_add_task(self) -> None:
        suite = BenchmarkSuite(name="test")
        task = BenchmarkTask(id="custom-001", name="Custom", description="", prompt="Hi")
        suite.add_task(task)
        assert len(suite) == 1
        assert suite.tasks[0].id == "custom-001"

    def test_summary(self) -> None:
        suite = BenchmarkSuite.all_builtins()
        summary = suite.summary()
        assert summary["count"] > 30
        assert "math" in summary["tags"]
