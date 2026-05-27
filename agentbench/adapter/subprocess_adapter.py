"""Adapter that runs an agent as a subprocess command."""

import shlex
import subprocess
import time

from agentbench.adapter.base import AgentAdapter, AgentRunResult


class SubprocessAdapter(AgentAdapter):
    """Runs an external CLI command for each prompt.

    The prompt is passed via stdin. The command's stdout capture is
    used as the agent's response.

    Args:
        command: Shell command to run. The prompt text is piped to stdin.
        name: Human-readable name for this adapter.
        timeout: Maximum seconds to wait for the subprocess.
    """

    def __init__(self, command: str, name: str | None = None, timeout: int = 60) -> None:
        self._command = command
        self.name = name or command
        self._timeout = timeout

    def run(self, prompt: str) -> AgentRunResult:
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                shlex.split(self._command),
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            duration = (time.perf_counter() - start) * 1000
            response = proc.stdout.strip() or proc.stderr.strip()
            return AgentRunResult(
                response=response,
                duration_ms=round(duration, 1),
                metadata={"return_code": proc.returncode},
            )
        except subprocess.TimeoutExpired:
            duration = (time.perf_counter() - start) * 1000
            return AgentRunResult(
                response="Error: subprocess timed out",
                duration_ms=round(duration, 1),
                metadata={"error": "timeout"},
            )
        except Exception as exc:
            duration = (time.perf_counter() - start) * 1000
            return AgentRunResult(
                response=f"Error: {exc}",
                duration_ms=round(duration, 1),
                metadata={"error": str(exc)},
            )
