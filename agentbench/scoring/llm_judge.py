"""LLM-as-judge scorer — uses a language model to evaluate response quality.

Requires the ``anthropic`` or ``openai`` SDK depending on the provider used.
"""

import json
import logging
import re
from typing import Any

from agentbench.scoring.base import Scorer, ScoreResult
from agentbench.tasks.base import BenchmarkTask

logger = logging.getLogger(__name__)

_JUDGE_PROMPT_TEMPLATE = """You are an expert evaluator of AI agent responses. Your job is to assess the quality, correctness, and completeness of a response to a given task.

## Task
{task_description}

## Task Prompt
{prompt}

## Reference / Expected Answer
{reference}

## Agent Response
{response}

## Rubric / Evaluation Criteria
{rubric}

## Instructions
Evaluate the agent's response based on the rubric above. Consider:
1. Correctness — does the answer address the task accurately?
2. Completeness — does it cover all required aspects?
3. Quality — is the reasoning sound and the presentation clear?

Respond with ONLY a valid JSON object in this exact format:
{{"score": <float between 0 and {max_score}>, "reasoning": "<brief explanation of the score>"}}

Do NOT include any text outside the JSON object.
"""


class LLMJudgeScorer(Scorer):
    """Uses an LLM to evaluate agent responses against a rubric.

    Args:
        judge_generator: A callable that accepts a list of message dicts
            (``[{"role": ..., "content": ...}, ...]``) and returns a
            text response string. Typically a wrapper around an LLM SDK.
        model: Model name for display/logging purposes.
    """

    def __init__(
        self,
        judge_generator: Any = None,
        model: str = "llm-judge",
    ) -> None:
        self._judge = judge_generator
        self._model = model

    def score(self, task: BenchmarkTask, response: str) -> ScoreResult:
        if self._judge is None:
            return ScoreResult(
                score=0.0,
                max_score=task.max_score,
                passed=False,
                details="LLM judge not configured — install anthropic or openai SDK and provide credentials",
            )

        prompt = _JUDGE_PROMPT_TEMPLATE.format(
            task_description=task.description,
            prompt=task.prompt,
            reference=task.reference,
            response=response[:4000],
            rubric=task.rubric or "Does the response correctly address the task?",
            max_score=task.max_score,
        )

        messages = [{"role": "user", "content": prompt}]

        try:
            raw = self._judge.generate(messages)
            parsed = self._parse_score(raw)
            score = parsed.get("score", 0.0)
            reasoning = parsed.get("reasoning", "")
            passed = score >= task.max_score * 0.7  # 70% threshold
            return ScoreResult(
                score=float(score),
                max_score=task.max_score,
                passed=passed,
                details=f"LLM judge ({self._model}): {reasoning}",
            )
        except Exception as exc:
            logger.exception("LLM judge scoring failed")
            return ScoreResult(
                score=0.0,
                max_score=task.max_score,
                passed=False,
                details=f"LLM judge error: {exc}",
            )

    @staticmethod
    def _parse_score(raw: str) -> dict[str, Any]:
        """Extract score dict from the judge's response."""
        cleaned = raw.strip()
        # Strip markdown fences
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```\w*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```$", "", cleaned)
        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback: try to extract a number
            match = re.search(r'"score"\s*:\s*([\d.]+)', cleaned)
            if match:
                return {"score": float(match.group(1)), "reasoning": "Extracted via regex fallback"}
            return {"score": 0.0, "reasoning": "Failed to parse judge response"}
