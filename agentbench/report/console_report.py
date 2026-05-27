"""Console-formatted benchmark reports using Rich."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

from agentbench.runner import BenchmarkReport

console = Console()


def print_console_report(report: BenchmarkReport, output_dir: str | Path | None = None) -> None:
    """Print a formatted benchmark report to the terminal."""
    # Summary header
    summary = (
        f"[bold]Suite:[/] {report.suite_name}\n"
        f"[bold]Agent:[/] {report.agent_name}\n"
        f"[bold]Timestamp:[/] {report.timestamp}\n"
        f"[bold]Duration:[/] {report.total_duration_ms:.0f} ms\n"
        f"[bold]Cost:[/] ${report.total_cost:.6f}"
    )
    console.print(Panel(summary, title="[bold]Benchmark Results[/]", border_style="blue"))

    # Overall score
    pct = report.overall_percentage
    color = "green" if pct >= 80 else "yellow" if pct >= 50 else "red"
    console.print(
        f"\n[bold]Overall:[/] [{color}]{pct:.1f}%[/]  "
        f"([green]{report.passed_count}[/]/[bold]{report.total_count}[/] passed)"
    )

    # Progress bar for overall score
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    with progress:
        task_id = progress.add_task("Score", total=report.total_max_score or 1, completed=report.total_score)

    # Per-task results table
    if report.results:
        table = Table(title="Per-Task Results", show_lines=True)
        table.add_column("ID", style="dim", width=12)
        table.add_column("Task", width=28)
        table.add_column("Score", justify="center", width=10)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Duration", justify="right", width=10)

        for r in report.results:
            status = "[green]PASS[/]" if r.score.passed else "[red]FAIL[/]"
            score_str = f"{r.score.percentage:.0f}%" if r.score.max_score > 0 else "-"
            table.add_row(
                r.task.id,
                r.task.name,
                score_str,
                status,
                f"{r.duration_ms:.0f}ms",
            )

        console.print("\n")
        console.print(table)

    # Output location
    if output_dir:
        console.print(f"\n[dim]Reports saved to: {output_dir}[/]")
