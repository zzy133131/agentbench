"""Central task registry — manages all registered benchmark tasks."""

import json
from typing import Any

from agentbench.tasks.base import BenchmarkTask, ScoringMethod

# Global task registry: id -> BenchmarkTask
_TASKS: dict[str, BenchmarkTask] = {}


def register_task(task: BenchmarkTask) -> None:
    """Register a single task in the global registry."""
    _TASKS[task.id] = task


def register_tasks(tasks: list[BenchmarkTask]) -> None:
    """Register multiple tasks at once."""
    for task in tasks:
        register_task(task)


def get_task(task_id: str) -> BenchmarkTask | None:
    """Look up a task by its ID."""
    return _TASKS.get(task_id)


def get_all_tasks() -> list[BenchmarkTask]:
    """Return all registered tasks."""
    return list(_TASKS.values())


def get_tasks_by_tag(tag: str) -> list[BenchmarkTask]:
    """Return all tasks that have the specified tag."""
    return [t for t in _TASKS.values() if tag in t.tags]


def get_tasks_by_tags(tags: list[str], mode: str = "any") -> list[BenchmarkTask]:
    """Return tasks matching a list of tags.

    Args:
        tags: Tag names to filter by.
        mode: ``"any"`` matches tasks with at least one of the given tags.
            ``"all"`` matches tasks that have every tag.
    """
    if mode == "all":
        return [t for t in _TASKS.values() if all(tag in t.tags for tag in tags)]
    return [t for t in _TASKS.values() if any(tag in t.tags for tag in tags)]


def load_tasks_from_json(path: str) -> list[BenchmarkTask]:
    """Load tasks from a JSON file.

    Expected JSON format::

        [
            {
                "id": "custom-001",
                "name": "...",
                "description": "...",
                "prompt": "...",
                "reference": "...",
                "scoring": "exact_match",
                "tags": ["custom"],
                "max_score": 1.0
            }
        ]
    """
    with open(path) as f:
        data: list[dict[str, Any]] = json.load(f)

    tasks = []
    for item in data:
        scoring_str = item.get("scoring", "exact_match")
        scoring = ScoringMethod(scoring_str)
        tasks.append(
            BenchmarkTask(
                id=item["id"],
                name=item.get("name", item["id"]),
                description=item.get("description", ""),
                prompt=item["prompt"],
                reference=item.get("reference", ""),
                scoring=scoring,
                rubric=item.get("rubric", ""),
                tags=item.get("tags", []),
                max_score=item.get("max_score", 1.0),
                metadata=item.get("metadata", {}),
            )
        )
    return tasks


def count_tasks() -> int:
    """Return the total number of registered tasks."""
    return len(_TASKS)


def list_tags() -> list[str]:
    """Return a sorted list of all unique tags across registered tasks."""
    tags: set[str] = set()
    for task in _TASKS.values():
        tags.update(task.tags)
    return sorted(tags)


# ---------------------------------------------------------------------------
# Auto-register built-in tasks on import
# ---------------------------------------------------------------------------
from agentbench.tasks.math import MATH_TASKS
from agentbench.tasks.reasoning import REASONING_TASKS
from agentbench.tasks.coding import CODING_TASKS
from agentbench.tasks.tool_use import TOOL_USE_TASKS

register_tasks(MATH_TASKS)
register_tasks(REASONING_TASKS)
register_tasks(CODING_TASKS)
register_tasks(TOOL_USE_TASKS)
