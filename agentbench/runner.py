"""Benchmark runner — orchestrates agent evaluation across a task suite."""

import csv
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentbench.adapter.base import AgentAdapter, AgentRunResult
from agentbench.scoring.base import Scorer, ScoreResult
from agentbench.scoring.exact_match import ContainsScorer, ExactMatchScorer
from agentbench.scoring.llm_judge import LLMJudgeScorer
from agentbench.suite import BenchmarkSuite
from agentbench.tasks.base import BenchmarkTask, ScoringMethod

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """Result of evaluating one task against one agent."""

    task: BenchmarkTask
    response: str
    score: ScoreResult
    duration_ms: float = 0.0
    cost: float = 0.0


@dataclass
class BenchmarkReport:
    """Complete results of a benchmark run."""

    suite_name: str
    agent_name: str
    timestamp: str
    results: list[TaskResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    total_cost: float = 0.0

    @property
    def total_score(self) -> float:
        return sum(r.score.score for r in self.results)

    @property
    def total_max_score(self) -> float:
        return sum(r.score.max_score for r in self.results)

    @property
    def overall_percentage(self) -> float:
        if self.total_max_score <= 0:
            return 0.0
        return (self.total_score / self.total_max_score) * 100

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.score.passed)

    @property
    def total_count(self) -> int:
        return len(self.results)

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite": self.suite_name,
            "agent": self.agent_name,
            "timestamp": self.timestamp,
            "overall_percentage": round(self.overall_percentage, 1),
            "passed": self.passed_count,
            "total": self.total_count,
            "total_duration_ms": round(self.total_duration_ms, 1),
            "total_cost": round(self.total_cost, 6),
            "results": [
                {
                    "task_id": r.task.id,
                    "task_name": r.task.name,
                    "score": r.score.score,
                    "max_score": r.score.max_score,
                    "passed": r.score.passed,
                    "details": r.score.details,
                    "duration_ms": round(r.duration_ms, 1),
                    "response_preview": r.response[:200],
                }
                for r in self.results
            ],
        }

    def to_json(self, path: str | Path) -> None:
        """Export results to a JSON file."""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def to_csv(self, path: str | Path) -> None:
        """Export results to a CSV file."""
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["task_id", "task_name", "score", "max_score", "passed", "details", "duration_ms"])
            for r in self.results:
                writer.writerow([
                    r.task.id,
                    r.task.name,
                    r.score.score,
                    r.score.max_score,
                    r.score.passed,
                    r.score.details,
                    round(r.duration_ms, 1),
                ])


class BenchmarkRunner:
    """Orchestrates the evaluation of an agent against a suite of tasks.

    Args:
        suite: The set of tasks to evaluate against.
        scorers: Mapping of ScoringMethod -> Scorer. Falls back to defaults
            for missing methods.
    """

    def __init__(
        self,
        suite: BenchmarkSuite,
        scorers: dict[ScoringMethod, Scorer] | None = None,
    ) -> None:
        self.suite = suite
        self._scorers = scorers or {}

    def run(self, agent: AgentAdapter) -> BenchmarkReport:
        """Evaluate *agent* against every task in the suite.

        Returns a :class:`BenchmarkReport` with per-task results.
        """
        from datetime import UTC, datetime

        logger.info("Starting benchmark: suite='%s' agent='%s' (%d tasks)", self.suite.name, agent.name, len(self.suite))

        results: list[TaskResult] = []
        total_start = time.perf_counter()
        total_cost = 0.0

        for i, task in enumerate(self.suite.tasks, 1):
            logger.info("  [%d/%d] %s — %s", i, len(self.suite), task.id, task.name)

            task_start = time.perf_counter()
            agent_result: AgentRunResult = agent.run(task.prompt)
            task_duration = (time.perf_counter() - task_start) * 1000

            scorer = self._get_scorer(task.scoring)
            score_result = scorer.score(task, agent_result.response)

            results.append(
                TaskResult(
                    task=task,
                    response=agent_result.response,
                    score=score_result,
                    duration_ms=round(task_duration, 1),
                    cost=agent_result.cost,
                )
            )
            total_cost += agent_result.cost

        total_duration = (time.perf_counter() - total_start) * 1000

        return BenchmarkReport(
            suite_name=self.suite.name,
            agent_name=agent.name,
            timestamp=datetime.now(UTC).isoformat(),
            results=results,
            total_duration_ms=round(total_duration, 1),
            total_cost=round(total_cost, 6),
        )

    def _get_scorer(self, method: ScoringMethod) -> Scorer:
        """Return the appropriate scorer for the given method."""
        if method in self._scorers:
            return self._scorers[method]
        if method == ScoringMethod.EXACT_MATCH:
            return ExactMatchScorer()
        if method == ScoringMethod.CONTAINS:
            return ContainsScorer()
        if method == ScoringMethod.LLM_JUDGE:
            return LLMJudgeScorer()
        raise ValueError(f"Unknown scoring method: {method}")
