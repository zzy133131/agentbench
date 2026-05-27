"""Tests for task definitions and the registry."""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod
from agentbench.tasks.registry import (
    count_tasks,
    get_all_tasks,
    get_task,
    get_tasks_by_tag,
    list_tags,
    register_task,
    register_tasks,
)


class TestBenchmarkTask:
    def test_minimal_construction(self) -> None:
        task = BenchmarkTask(id="test-001", name="Test", description="A test", prompt="Hello?")
        assert task.id == "test-001"
        assert task.name == "Test"
        assert task.scoring == ScoringMethod.EXACT_MATCH
        assert task.max_score == 1.0
        assert task.tags == []
        assert task.reference == ""

    def test_full_construction(self) -> None:
        task = BenchmarkTask(
            id="test-002",
            name="Full Test",
            description="A full test",
            prompt="Do something",
            reference="42",
            scoring=ScoringMethod.CONTAINS,
            tags=["math", "test"],
            max_score=5.0,
            rubric="Check correctness",
        )
        assert task.scoring == ScoringMethod.CONTAINS
        assert task.max_score == 5.0
        assert task.rubric == "Check correctness"


class TestRegistry:
    def test_builtin_tasks_are_registered(self) -> None:
        """Built-in tasks should auto-register on import."""
        assert count_tasks() > 30  # math + reasoning + coding + tool_use

    def test_get_all_tasks(self) -> None:
        tasks = get_all_tasks()
        assert len(tasks) == count_tasks()

    def test_get_task(self) -> None:
        task = get_task("math-001")
        assert task is not None
        assert task.name == "Basic addition"

    def test_get_nonexistent_task(self) -> None:
        assert get_task("nonexistent") is None

    def test_get_tasks_by_tag(self) -> None:
        math_tasks = get_tasks_by_tag("math")
        assert len(math_tasks) >= 10
        assert all("math" in t.tags for t in math_tasks)

    def test_list_tags(self) -> None:
        tags = list_tags()
        assert "math" in tags
        assert "reasoning" in tags
        assert "coding" in tags
        assert "tool-use" in tags

    def test_register_single_task(self) -> None:
        task = BenchmarkTask(
            id="registry-test-001",
            name="Registry Test",
            description="Testing registration",
            prompt="Test prompt",
        )
        register_task(task)
        assert get_task("registry-test-001") is task

        # Clean up internal registry state
        from agentbench.tasks.registry import _TASKS

        _TASKS.pop("registry-test-001", None)

    def test_register_multiple_tasks(self) -> None:
        tasks = [
            BenchmarkTask(id="multi-001", name="A", description="", prompt="P1"),
            BenchmarkTask(id="multi-002", name="B", description="", prompt="P2"),
        ]
        register_tasks(tasks)
        assert get_task("multi-001") is not None
        assert get_task("multi-002") is not None

        from agentbench.tasks.registry import _TASKS

        _TASKS.pop("multi-001", None)
        _TASKS.pop("multi-002", None)
