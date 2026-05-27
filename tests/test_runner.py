"""Tests for BenchmarkRunner."""

from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.runner import BenchmarkRunner
from agentbench.suite import BenchmarkSuite


def test_runner_returns_report() -> None:
    suite = BenchmarkSuite.by_ids(["math-001", "math-002"])
    adapter = FunctionAdapter(lambda p: "42", name="AnswerBot")
    runner = BenchmarkRunner(suite=suite)
    report = runner.run(adapter)

    assert report.suite_name == suite.name
    assert report.agent_name == "AnswerBot"
    assert report.total_count == 2
    assert report.total_max_score == 2.0
    assert report.timestamp is not None


def test_runner_scoring() -> None:
    suite = BenchmarkSuite.by_ids(["math-001"])  # 123 + 456 = 579
    adapter = FunctionAdapter(lambda p: "579", name="SmartBot")
    runner = BenchmarkRunner(suite=suite)
    report = runner.run(adapter)

    assert report.passed_count == 1
    assert report.total_score == 1.0
    assert report.overall_percentage == 100.0


def test_runner_failure() -> None:
    suite = BenchmarkSuite.by_ids(["math-001"])  # 123 + 456 = 579
    adapter = FunctionAdapter(lambda p: "wrong answer", name="DumbBot")
    runner = BenchmarkRunner(suite=suite)
    report = runner.run(adapter)

    assert report.passed_count == 0
    assert report.total_score == 0.0


def test_report_to_dict() -> None:
    suite = BenchmarkSuite.by_ids(["math-001"])
    adapter = FunctionAdapter(lambda p: "579", name="TestBot")
    runner = BenchmarkRunner(suite=suite)
    report = runner.run(adapter)

    d = report.to_dict()
    assert d["agent"] == "TestBot"
    assert d["overall_percentage"] == 100.0
    assert d["passed"] == 1
    assert d["total"] == 1
    assert len(d["results"]) == 1
