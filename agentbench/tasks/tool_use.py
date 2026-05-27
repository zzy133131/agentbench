"""Tool-use and function-calling benchmark tasks.

These tasks test an agent's ability to use tools appropriately.
They are best evaluated with LLM-as-judge scoring since there may be
multiple valid approaches.
"""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod

TOOL_USE_TASKS = [
    BenchmarkTask(
        id="tool-001",
        name="Calculator usage",
        description="Agent should use a calculator tool for arithmetic",
        prompt=(
            "You have access to a calculator tool. "
            "Use it to compute 12345 × 6789 and tell me the result."
        ),
        scoring=ScoringMethod.CONTAINS,
        reference="83810205",
        tags=["tool-use", "calculator"],
    ),
    BenchmarkTask(
        id="tool-002",
        name="Data transformation",
        description="Agent should use a tool to process CSV data",
        prompt=(
            "I have this CSV data:\n"
            "name,age,city\n"
            "Alice,30,New York\n"
            "Bob,25,London\n"
            "Charlie,35,Tokyo\n\n"
            "Use a file tool to save this to a file called 'people.csv', "
            "then read it back and tell me the average age."
        ),
        scoring=ScoringMethod.CONTAINS,
        reference="30",
        tags=["tool-use", "file-ops"],
    ),
    BenchmarkTask(
        id="tool-003",
        name="Code execution",
        description="Agent should use a code execution tool to solve a problem",
        prompt=(
            "Use a Python execution tool to find all prime numbers between 1 and 50. "
            "List them as a comma-separated list."
        ),
        scoring=ScoringMethod.CONTAINS,
        reference="2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47",
        tags=["tool-use", "code-execution"],
    ),
    BenchmarkTask(
        id="tool-004",
        name="Multi-tool workflow",
        description="Agent should combine multiple tools to complete a complex task",
        prompt=(
            "Write a Python script that generates the first 20 Fibonacci numbers, "
            "save the script to a file called 'fib.py', and then execute it. "
            "Show me both the script and its output."
        ),
        scoring=ScoringMethod.CONTAINS,
        reference="4181",
        tags=["tool-use", "multi-step"],
    ),
    BenchmarkTask(
        id="tool-005",
        name="Web fetch",
        description="Agent should fetch and extract information from a URL",
        prompt=(
            "Fetch the content from https://example.com and tell me the page title."
        ),
        scoring=ScoringMethod.CONTAINS,
        reference="Example Domain",
        tags=["tool-use", "web"],
    ),
]
