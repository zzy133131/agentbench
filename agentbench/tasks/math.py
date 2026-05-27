"""Mathematical reasoning benchmark tasks."""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod

MATH_TASKS = [
    BenchmarkTask(
        id="math-001",
        name="Basic addition",
        description="Add two three-digit numbers",
        prompt="What is 123 + 456? Answer with just the number.",
        reference="579",
        tags=["math", "arithmetic"],
    ),
    BenchmarkTask(
        id="math-002",
        name="Multiplication",
        description="Multiply two two-digit numbers",
        prompt="What is 15 × 27? Answer with just the number.",
        reference="405",
        tags=["math", "arithmetic"],
    ),
    BenchmarkTask(
        id="math-003",
        name="Division",
        description="Divide two numbers",
        prompt="What is 144 ÷ 12? Answer with just the number.",
        reference="12",
        tags=["math", "arithmetic"],
    ),
    BenchmarkTask(
        id="math-004",
        name="Exponentiation",
        description="Calculate a power",
        prompt="What is 2 to the power of 10? Answer with just the number.",
        reference="1024",
        tags=["math", "arithmetic"],
    ),
    BenchmarkTask(
        id="math-005",
        name="Square root",
        description="Calculate a square root",
        prompt="What is the square root of 121? Answer with just the number.",
        reference="11",
        tags=["math", "arithmetic"],
    ),
    BenchmarkTask(
        id="math-006",
        name="Percentage",
        description="Calculate a percentage",
        prompt="What is 15% of 200? Answer with just the number.",
        reference="30",
        tags=["math", "percentage"],
    ),
    BenchmarkTask(
        id="math-007",
        name="Word problem — distance",
        description="Solve a distance = rate × time word problem",
        prompt=(
            "If a train travels at 60 miles per hour for 2.5 hours, "
            "how many miles does it travel? Answer with just the number."
        ),
        reference="150",
        tags=["math", "word-problem"],
    ),
    BenchmarkTask(
        id="math-008",
        name="Fraction addition",
        description="Add two fractions",
        prompt="What is 3/4 + 1/3? Give your answer as a simplified fraction.",
        reference="13/12",
        tags=["math", "fractions"],
    ),
    BenchmarkTask(
        id="math-009",
        name="Factorial",
        description="Calculate a factorial",
        prompt="What is 7! (7 factorial)? Answer with just the number.",
        reference="5040",
        tags=["math", "combinatorics"],
    ),
    BenchmarkTask(
        id="math-010",
        name="Multi-step arithmetic",
        description="Solve a multi-step arithmetic expression with correct order of operations",
        prompt="What is (8 + 2) × (6 − 4) + 3²? Answer with just the number.",
        reference="29",
        tags=["math", "order-of-operations"],
    ),
    BenchmarkTask(
        id="math-011",
        name="Compound interest",
        description="Calculate compound interest",
        prompt=(
            "If you invest $1000 at an annual interest rate of 5%% compounded annually "
            "for 3 years, what is the total amount? Round to the nearest dollar. "
            "Answer with just the number (no $ sign)."
        ),
        reference="1158",
        tags=["math", "finance"],
    ),
    BenchmarkTask(
        id="math-012",
        name="System of equations",
        description="Solve a simple system of two linear equations",
        prompt=(
            "Solve for x and y: x + y = 10 and 2x − y = 5. "
            "Answer as 'x=<value>, y=<value>'."
        ),
        reference="x=5, y=5",
        tags=["math", "algebra"],
    ),
]
