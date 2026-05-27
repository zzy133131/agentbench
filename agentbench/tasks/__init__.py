"""Built-in benchmark task definitions."""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod
from agentbench.tasks.registry import (
    get_all_tasks,
    get_task,
    get_tasks_by_tag,
    load_tasks_from_json,
    register_task,
    register_tasks,
)

__all__ = [
    "BenchmarkTask",
    "ScoringMethod",
    "get_all_tasks",
    "get_task",
    "get_tasks_by_tag",
    "load_tasks_from_json",
    "register_task",
    "register_tasks",
]
