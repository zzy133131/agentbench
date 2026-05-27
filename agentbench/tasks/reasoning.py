"""Logical reasoning and puzzle benchmark tasks."""

from agentbench.tasks.base import BenchmarkTask, ScoringMethod

REASONING_TASKS = [
    BenchmarkTask(
        id="reason-001",
        name="Basic syllogism",
        description="Evaluate a classical syllogism",
        prompt=(
            "All humans are mortal. Socrates is human. "
            "Is Socrates mortal? Answer yes or no."
        ),
        reference="yes",
        tags=["reasoning", "logic"],
    ),
    BenchmarkTask(
        id="reason-002",
        name="Sequence completion",
        description="Identify the next number in a geometric sequence",
        prompt=(
            "What is the next number in this sequence: 2, 6, 18, 54, ? "
            "Answer with just the number."
        ),
        reference="162",
        tags=["reasoning", "patterns"],
    ),
    BenchmarkTask(
        id="reason-003",
        name="Truth-teller puzzle",
        description="Solve a classic knight/knave logic puzzle",
        prompt=(
            "You meet two people: A and B. A says 'B is a liar.' "
            "B says 'A is a liar.' Exactly one of them tells the truth. "
            "Who is the truth-teller? Answer 'A' or 'B'."
        ),
        reference="A",
        scoring=ScoringMethod.EXACT_MATCH,
        tags=["reasoning", "logic-puzzle"],
    ),
    BenchmarkTask(
        id="reason-004",
        name="Anagram solver",
        description=" Solve a common word anagram",
        prompt=(
            "Unscramble the letters to form a common English word: 'PPLEA'. "
            "Answer with the word only."
        ),
        reference="apple",
        tags=["reasoning", "word-puzzle"],
    ),
    BenchmarkTask(
        id="reason-005",
        name="River crossing",
        description="Solve a river crossing puzzle",
        prompt=(
            "A farmer needs to cross a river with a wolf, a goat, and a cabbage. "
            "His boat can only carry him and one item at a time. "
            "If left alone, the wolf eats the goat and the goat eats the cabbage. "
            "What is the first item he should take across? Answer: wolf, goat, or cabbage."
        ),
        reference="goat",
        tags=["reasoning", "puzzle"],
    ),
    BenchmarkTask(
        id="reason-006",
        name="Calendar calculation",
        description="Determine what day of the week a date falls on, given a reference",
        prompt=(
            "If January 1 is a Monday, what day of the week is January 31? "
            "Answer with the day name only."
        ),
        reference="wednesday",
        tags=["reasoning", "calendar"],
    ),
    BenchmarkTask(
        id="reason-007",
        name="Coin weighing",
        description="Determine the minimum number of weighings needed",
        prompt=(
            "You have 9 identical-looking coins. One is counterfeit and weighs less "
            "than the others. You have a balance scale. "
            "What is the minimum number of weighings needed to guarantee finding "
            "the counterfeit? Answer with just the number."
        ),
        reference="2",
        tags=["reasoning", "puzzle"],
    ),
    BenchmarkTask(
        id="reason-008",
        name="Negation",
        description="Correctly negate a logical statement",
        prompt=(
            "What is the negation of 'All cats are mammals'? "
            "Answer exactly: 'There exists a cat that is not a mammal.' or "
            "'No cats are mammals.'"
        ),
        reference="There exists a cat that is not a mammal.",
        scoring=ScoringMethod.CONTAINS,
        tags=["reasoning", "logic"],
    ),
    BenchmarkTask(
        id="reason-009",
        name="Age word problem",
        description="Solve a simple age word problem",
        prompt=(
            "Alice is twice as old as Bob. In 5 years, the sum of their ages "
            "will be 40. How old is Alice now? Answer with just the number."
        ),
        reference="20",
        tags=["reasoning", "word-problem"],
    ),
    BenchmarkTask(
        id="reason-010",
        name="Spatial reasoning",
        description="Determine which way a person is facing after turns",
        prompt=(
            "A person is facing north. They turn 90 degrees to the right, "
            "then 180 degrees, then 90 degrees to the left. "
            "What direction are they now facing? Answer with the direction name only."
        ),
        reference="west",
        tags=["reasoning", "spatial"],
    ),
]
