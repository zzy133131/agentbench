"""Example: benchmark an agent using LLM-as-judge scoring.

Requires:
    pip install agentbench[claude]   (or [openai])
    export ANTHROPIC_API_KEY=sk-...

Usage:
    python examples/with_llm_judge.py
"""

from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.report.console_report import print_console_report
from agentbench.runner import BenchmarkRunner
from agentbench.scoring.exact_match import ContainsScorer, ExactMatchScorer
from agentbench.scoring.llm_judge import LLMJudgeScorer
from agentbench.suite import BenchmarkSuite
from agentbench.tasks.base import ScoringMethod


def _build_llm_judge():
    """Build an LLM judge using Claude (requires ANTHROPIC_API_KEY)."""
    try:
        from agentforge.llm.claude_provider import ClaudeProvider

        judge = ClaudeProvider()
        return LLMJudgeScorer(judge_generator=judge, model="claude-sonnet-4")
    except ImportError:
        print("Note: 'agentforge' not installed, using mock judge.")
        return None


def main() -> None:
    def my_agent(prompt: str) -> str:
        return f"This is my response to: {prompt[:60]}..."

    adapter = FunctionAdapter(my_agent, name="DemoAgent")

    # Suite with LLM-judge tasks
    suite = BenchmarkSuite.by_ids(["tool-001", "custom-001"])

    # Custom scorers (override defaults)
    scorers = {
        ScoringMethod.EXACT_MATCH: ExactMatchScorer(),
        ScoringMethod.CONTAINS: ContainsScorer(),
        ScoringMethod.LLM_JUDGE: _build_llm_judge(),
    }

    runner = BenchmarkRunner(suite=suite, scorers=scorers)
    report = runner.run(adapter)
    print_console_report(report)


if __name__ == "__main__":
    main()
