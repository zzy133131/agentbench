"""AgentBench CLI — run benchmarks from the terminal."""

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.report.console_report import print_console_report
from agentbench.report.html_report import generate_html_report
from agentbench.runner import BenchmarkRunner
from agentbench.suite import BenchmarkSuite
from agentbench.tasks.registry import count_tasks, list_tags

app = typer.Typer(help="AgentBench — evaluate and benchmark AI agents.")
console = Console()


@app.command()
def run(
    agent_name: str = typer.Option("agent", "--agent", "-a", help="Name of the agent under test"),
    suite_name: str = typer.Option("all", "--suite", "-s", help="Benchmark suite to run (all, math, reasoning, coding, tool_use, or tag name)"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Directory to save reports (JSON, CSV, HTML)"),
    html: bool = typer.Option(True, "--html/--no-html", help="Generate HTML report"),
    csv: bool = typer.Option(False, "--csv", help="Export results as CSV"),
    json: bool = typer.Option(False, "--json", help="Export results as JSON"),
    task_ids: Optional[str] = typer.Option(None, "--tasks", "-t", help="Comma-separated list of task IDs to run"),
) -> None:
    """Run a benchmark against a simple chatbot function.

    By default evaluates a minimal echo-agent against the full built-in
    suite. Bring your own agent by wrapping it with an adapter.
    """
    # Build suite
    if task_ids:
        ids = [t.strip() for t in task_ids.split(",")]
        suite = BenchmarkSuite.by_ids(ids, name=f"Custom ({len(ids)} tasks)")
    elif suite_name == "all":
        suite = BenchmarkSuite.all_builtins()
    elif suite_name in ("math", "reasoning", "coding", "tool_use"):
        suite = BenchmarkSuite.by_tag(suite_name)
    else:
        suite = BenchmarkSuite.by_tag(suite_name)

    if len(suite) == 0:
        rprint(f"[red]No tasks found for suite '{suite_name}'.[/]")
        rprint(f"Available tags: {', '.join(list_tags())}")
        raise typer.Exit(1)

    # Create a simple echo agent as default (replace with your own)
    def echo_agent(prompt: str) -> str:
        return f"You said: {prompt}"

    adapter = FunctionAdapter(echo_agent, name=agent_name)

    # Run benchmark
    runner = BenchmarkRunner(suite=suite)
    with console.status("[bold green]Running benchmark...[/]") as status:
        report = runner.run(adapter)

    # Output results
    output_path = Path(output_dir) if output_dir else None
    if output_path:
        output_path.mkdir(parents=True, exist_ok=True)

    print_console_report(report, output_dir=output_path)

    if output_path:
        if json:
            json_path = output_path / "results.json"
            report.to_json(json_path)
            console.print(f"  [dim]JSON:[/] {json_path}")
        if csv:
            csv_path = output_path / "results.csv"
            report.to_csv(csv_path)
            console.print(f"  [dim]CSV:[/] {csv_path}")
    if html and output_path:
        html_path = generate_html_report(report, output_path / "report.html")
        console.print(f"  [dim]HTML:[/] {html_path}")
    elif html:
        html_path = generate_html_report(report, Path("benchmark_report.html"))
        console.print(f"  [dim]HTML:[/] {html_path}")


@app.command()
def list_tasks(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
) -> None:
    """List all available benchmark tasks."""
    from agentbench.tasks.registry import get_all_tasks, get_tasks_by_tag

    tasks = get_tasks_by_tag(tag) if tag else get_all_tasks()

    if not tasks:
        rprint(f"[yellow]No tasks found{ ' for tag: ' + tag if tag else ''}.[/]")
        return

    table = Table(title=f"Benchmark Tasks ({len(tasks)} total)")
    table.add_column("ID", style="dim", width=14)
    table.add_column("Name", width=30)
    table.add_column("Scoring", width=14)
    table.add_column("Tags", width=30)

    for t in tasks:
        table.add_row(t.id, t.name, t.scoring.value, ", ".join(t.tags))

    console.print(table)


@app.command()
def info() -> None:
    """Show summary information about the installed benchmark suite."""
    from agentbench.tasks.registry import count_tasks, list_tags

    total = count_tasks()
    tags = list_tags()

    table = Table(title="AgentBench Info")
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Total tasks", str(total))
    table.add_row("Total tags", str(len(tags)))
    table.add_row("Tags", ", ".join(tags))
    table.add_row("Version", "0.1.0")

    console.print(table)


@app.command()
def compare(
    results: list[str] = typer.Argument(..., help="Paths to JSON result files"),
) -> None:
    """Compare results from multiple benchmark runs."""
    import json

    table = Table(title="Benchmark Comparison")
    table.add_column("Metric", style="bold")

    data = []
    for path in results:
        with open(path) as f:
            data.append(json.load(f))
        table.add_column(f"Run {len(data)}", justify="center")

    if data:
        table.add_row("Agent", *[d.get("agent", "?") for d in data])
        table.add_row("Suite", *[d.get("suite", "?") for d in data])
        table.add_row(
            "Score (%)",
            *[f"{d.get('overall_percentage', 0):.1f}%" for d in data],
        )
        table.add_row("Passed", *[f"{d.get('passed', 0)}/{d.get('total', 0)}" for d in data])
        table.add_row("Duration (ms)", *[f"{d.get('total_duration_ms', 0):.0f}" for d in data])
        table.add_row("Cost ($)", *[f"{d.get('total_cost', 0):.6f}" for d in data])

    console.print(table)


if __name__ == "__main__":
    app()
