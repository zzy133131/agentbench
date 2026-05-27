"""Example: benchmark a simple echo agent against the full task suite.

Usage:
    python examples/run_benchmark.py
"""

from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.report.console_report import print_console_report
from agentbench.report.html_report import generate_html_report
from agentbench.runner import BenchmarkRunner
from agentbench.suite import BenchmarkSuite


def main() -> None:
    # --- Define a simple agent ---
    # Replace this with any function that takes a prompt and returns a response.
    def my_agent(prompt: str) -> str:
        # A very basic agent that just echoes with a prefix
        return f"I understand you're asking about: {prompt[:100]}..."

    adapter = FunctionAdapter(my_agent, name="EchoAgent")

    # --- Pick a suite ---
    suite = BenchmarkSuite.by_tag("math", name="Math Problems")

    # --- Run the benchmark ---
    runner = BenchmarkRunner(suite=suite)
    report = runner.run(adapter)

    # --- Print results ---
    print_console_report(report)

    # --- Save HTML report ---
    path = generate_html_report(report, "benchmark_report.html")
    print(f"\nHTML report saved to: {path}")


if __name__ == "__main__":
    main()
