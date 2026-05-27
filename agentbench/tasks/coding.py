"""Code generation and programming benchmark tasks."""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod

CODING_TASKS = [
    BenchmarkTask(
        id="code-001",
        name="Palindrome check",
        description="Write a function to check if a string is a palindrome",
        prompt=(
            "Write a Python function called is_palindrome(s) that returns True "
            "if the string s is a palindrome (reads the same forwards and backwards), "
            "False otherwise. Ignore case and non-alphanumeric characters. "
            "Provide just the function, no explanation."
        ),
        reference="is_palindrome",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "algorithms"],
    ),
    BenchmarkTask(
        id="code-002",
        name="Prime number check",
        description="Write a function to check if a number is prime",
        prompt=(
            "Write a Python function called is_prime(n) that returns True if n is a "
            "prime number, False otherwise. Provide just the function definition."
        ),
        reference="is_prime",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "algorithms"],
    ),
    BenchmarkTask(
        id="code-003",
        name="Fibonacci sequence",
        description="Generate the nth Fibonacci number",
        prompt=(
            "Write a Python function called fibonacci(n) that returns the "
            "nth number in the Fibonacci sequence (0-indexed, so fibonacci(0) = 0, "
            "fibonacci(1) = 1). Provide just the function."
        ),
        reference="fibonacci",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "algorithms"],
    ),
    BenchmarkTask(
        id="code-004",
        name="FizzBuzz",
        description="Implement the classic FizzBuzz problem",
        prompt=(
            "Write a Python function called fizzbuzz(n) that prints numbers from 1 to n, "
            "but for multiples of 3 print 'Fizz' instead, for multiples of 5 print 'Buzz', "
            "and for multiples of both print 'FizzBuzz'. Provide just the function."
        ),
        reference="fizzbuzz",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python"],
    ),
    BenchmarkTask(
        id="code-005",
        name="Word frequency counter",
        description="Count word frequencies in a sentence",
        prompt=(
            "Write a Python function called word_count(text) that returns a dictionary "
            "with each word as a key and its frequency as the value. Ignore case and "
            "punctuation. Provide just the function."
        ),
        reference="word_count",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "strings"],
    ),
    BenchmarkTask(
        id="code-006",
        name="Binary search",
        description="Implement binary search on a sorted array",
        prompt=(
            "Write a Python function called binary_search(arr, target) that performs "
            "binary search on a sorted list and returns the index of the target, or -1 "
            "if not found. Provide just the function."
        ),
        reference="binary_search",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "algorithms"],
    ),
    BenchmarkTask(
        id="code-007",
        name="SQL query — SELECT",
        description="Write a SQL query to select filtered data",
        prompt=(
            "Write a SQL query to select all employees from the 'employees' table "
            "whose salary is greater than 50000, ordered by last name ascending. "
            "Provide just the SQL query, no explanation."
        ),
        reference="SELECT",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "sql"],
    ),
    BenchmarkTask(
        id="code-008",
        name="Regex email validation",
        description="Write a regex pattern for validating email addresses",
        prompt=(
            "Write a Python function called is_valid_email(email) that uses a regular "
            "expression to check if an email address is valid (has exactly one @, "
            "a domain with at least one dot, etc.). Provide just the function."
        ),
        reference="is_valid_email",
        scoring=ScoringMethod.CONTAINS,
        tags=["coding", "python", "regex"],
    ),
]
