# AgentBench

## Project Introduction / 项目介绍

**English:** AgentBench is a framework for benchmarking and evaluating AI agents with comprehensive test suites. It helps teams measure, compare, and improve agents across math, reasoning, coding, and tool-use capabilities with repeatable scoring and reports.

**中文：** AgentBench 是一个用于基准测试和评估 AI 智能体的框架，内置覆盖数学、推理、代码生成和工具使用能力的测试套件。它通过可复现的评分与报告，帮助团队衡量、比较并持续改进智能体表现。

## Features

- **35+ Built-in Tasks** — Benchmarks spanning math, logical reasoning, code generation, and tool use
- **Multiple Scoring Methods** — Exact match, substring containment, and LLM-as-judge evaluation
- **Rich Reports** — Console output with progress bars + standalone HTML reports with visual summaries
- **Adaptable** — Adapter pattern lets you benchmark any agent (function, CLI, API, or framework)
- **Custom Suites** — Define your own tasks in JSON or via the Python API
- **Comparison Mode** — Compare results across multiple benchmark runs
- **Lightweight** — Pure Python with minimal dependencies

## Quick Start

```bash
# Install from source
cd agentbench
pip install -e .

# With optional LLM judge:
pip install -e ".[claude]"   # For LLM-as-judge using Claude
pip install -e ".[openai]"   # For LLM-as-judge using GPT-4
```

### Basic Usage

```bash
# Run the full benchmark suite
agentbench run --agent "MyAgent"

# Run a specific suite
agentbench run --suite math
agentbench run --suite reasoning

# Run specific tasks by ID
agentbench run --tasks "math-001,math-002,reason-001"

# Save reports
agentbench run --output ./results --json --csv
```

### Python API

```python
from agentbench.adapter.function_adapter import FunctionAdapter
from agentbench.runner import BenchmarkRunner
from agentbench.suite import BenchmarkSuite

# Define your agent
def my_agent(prompt: str) -> str:
    return f"Answer to: {prompt}"

adapter = FunctionAdapter(my_agent, name="MyAgent")

# Pick a suite
suite = BenchmarkSuite.by_tag("math")

# Run benchmark
runner = BenchmarkRunner(suite=suite)
report = runner.run(adapter)

# Print results
print(f"Score: {report.overall_percentage:.1f}%")
print(f"Passed: {report.passed_count}/{report.total_count}")
```

## Built-in Tasks

| Suite | Count | Description |
|-------|-------|-------------|
| Math | 12 | Arithmetic, algebra, percentages, word problems |
| Reasoning | 10 | Logic puzzles, sequences, syllogisms, spatial reasoning |
| Coding | 8 | Algorithms, FizzBuzz, SQL, regex, data structures |
| Tool Use | 5 | Calculator, file ops, code execution, multi-tool workflows |

## Scoring Methods

| Method | Description |
|--------|-------------|
| `exact_match` | Case-insensitive exact string match against reference |
| `contains` | Reference string must appear in the response |
| `llm_judge` | An LLM evaluates response quality against a rubric |

## Custom Task Suites

Define tasks in JSON:

```json
[
    {
        "id": "my-task-001",
        "name": "Custom question",
        "description": "Test specific knowledge",
        "prompt": "What is the capital of France?",
        "reference": "Paris",
        "scoring": "exact_match",
        "tags": ["custom", "geography"],
        "max_score": 1.0
    }
]
```

Load and run:

```bash
agentbench run --suite custom --tasks "my-task-001"
```

Or via Python:

```python
suite = BenchmarkSuite.from_json("custom_tasks.json")
```

## Architecture

```
┌──────────────────────────────────────────────────┐
│              BenchmarkRunner                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │  Suite   │→ │ Adapter  │→ │    Scorer      │  │
│  │ (Tasks)  │  │ (Agent)  │  │ (Evaluation)   │  │
│  └──────────┘  └──────────┘  └────────────────┘  │
│                        ↓                          │
│                  BenchmarkReport                   │
│              (JSON / CSV / HTML)                   │
└──────────────────────────────────────────────────┘
```

## CLI Commands

```bash
# List all tasks
agentbench list-tasks

# List tasks by tag
agentbench list-tasks --tag math

# Show benchmark suite info
agentbench info

# Compare multiple result files
agentbench compare results1.json results2.json
```

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `BenchmarkTask` | A single evaluation task (prompt, reference, scoring method) |
| `BenchmarkSuite` | A named collection of tasks with factory constructors |
| `BenchmarkRunner` | Orchestrates agent evaluation across a task suite |
| `BenchmarkReport` | Complete results including per-task scores and metadata |

### Adapters

| Adapter | Description |
|---------|-------------|
| `FunctionAdapter` | Wraps any Python callable as an agent |
| `SubprocessAdapter` | Runs an external CLI command for each prompt |

### Scorers

| Scorer | Description |
|--------|-------------|
| `ExactMatchScorer` | Case-insensitive equality check |
| `ContainsScorer` | Substring presence check |
| `LLMJudgeScorer` | LLM-based quality evaluation with rubric |

## Running Tests

```bash
pip install pytest
pytest tests/
```

## Project Structure

```
agentbench/
├── agentbench/
│   ├── tasks/          # Benchmark task definitions (math, reasoning, coding, tool_use)
│   ├── scoring/        # Scoring mechanisms (exact match, contains, LLM judge)
│   ├── adapter/        # Agent adapters (function, subprocess)
│   ├── report/         # Report generation (console, HTML)
│   ├── cli/            # CLI interface
│   ├── runner.py       # Benchmark orchestration
│   └── suite.py        # Task suite management
├── examples/           # Usage examples
├── tests/              # Test suite
└── pyproject.toml      # Project metadata
```

## Use Cases

- **Agent Development** — Measure improvements as you iterate on prompts and tools
- **Regression Testing** — Catch regressions before deploying agent updates
- **Model Comparison** — Compare different LLMs on the same benchmark suite
- **Custom Evaluations** — Create domain-specific benchmarks for your use case
- **CI Integration** — Run benchmarks automatically on every commit

## License

MIT
