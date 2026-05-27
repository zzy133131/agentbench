"""Benchmark suite — selects task subsets for evaluation."""

from typing import Any

from agentbench.tasks.base import BenchmarkTask
from agentbench.tasks.registry import (
    get_all_tasks,
    get_tasks_by_tag,
    get_tasks_by_tags,
    load_tasks_from_json,
    register_tasks,
)


class BenchmarkSuite:
    """A named collection of benchmark tasks.

    A suite can be a subset of the global task registry, custom tasks
    loaded from a JSON file, or a combination of both.

    Args:
        name: Human-readable name for this suite (used in reports).
        tasks: Pre-built list of tasks for this suite.
    """

    def __init__(self, name: str = "default", tasks: list[BenchmarkTask] | None = None) -> None:
        self.name = name
        self._tasks: list[BenchmarkTask] = tasks or []

    # ------------------------------------------------------------------
    # Factory constructors
    # ------------------------------------------------------------------

    @classmethod
    def all_builtins(cls, name: str = "All Built-in Tasks") -> "BenchmarkSuite":
        """Suite containing every registered built-in task."""
        return cls(name=name, tasks=get_all_tasks())

    @classmethod
    def by_tag(cls, tag: str, name: str | None = None) -> "BenchmarkSuite":
        """Suite containing tasks that match a tag (e.g. ``"math"``)."""
        display = name or f"Tag: {tag}"
        return cls(name=display, tasks=get_tasks_by_tag(tag))

    @classmethod
    def by_tags(cls, tags: list[str], mode: str = "any", name: str | None = None) -> "BenchmarkSuite":
        """Suite containing tasks matching a list of tags."""
        display = name or f"Tags: {', '.join(tags)} ({mode})"
        return cls(name=display, tasks=get_tasks_by_tags(tags, mode=mode))

    @classmethod
    def from_json(cls, path: str, name: str | None = None) -> "BenchmarkSuite":
        """Suite loaded from a JSON file of custom tasks."""
        tasks = load_tasks_from_json(path)
        register_tasks(tasks)
        display = name or f"Custom: {path}"
        return cls(name=display, tasks=tasks)

    @classmethod
    def by_ids(cls, task_ids: list[str], name: str | None = None) -> "BenchmarkSuite":
        """Suite containing specific tasks by their IDs."""
        from agentbench.tasks.registry import get_task

        tasks = [get_task(tid) for tid in task_ids if get_task(tid) is not None]
        display = name or f"Custom ({len(tasks)} tasks)"
        return cls(name=display, tasks=tasks)

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------

    @property
    def tasks(self) -> list[BenchmarkTask]:
        return list(self._tasks)

    @tasks.setter
    def tasks(self, value: list[BenchmarkTask]) -> None:
        self._tasks = list(value)

    def add_task(self, task: BenchmarkTask) -> None:
        """Add a single task to this suite."""
        self._tasks.append(task)

    def summary(self) -> dict[str, Any]:
        """Return summary statistics about the suite."""
        tag_counts: dict[str, int] = {}
        for t in self._tasks:
            for tag in t.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return {
            "name": self.name,
            "count": len(self._tasks),
            "tags": tag_counts,
            "scoring_methods": {
                scoring: sum(1 for t in self._tasks if t.scoring.value == scoring)
                for scoring in {t.scoring.value for t in self._tasks}
            },
        }

    def __len__(self) -> int:
        return len(self._tasks)
