from __future__ import annotations

import hashlib
import json
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any


class AgentError(RuntimeError):
    pass


class CommandAgentProvider:
    """Run an independent ephemeral Codex process and retain its trace."""

    def __init__(self, workspace: Path, log_dir: Path, executable: str,
                 model: str, reasoning_effort: str, timeout_seconds: int,
                 disable_nested_agents: bool = True):
        if reasoning_effort not in {"minimal", "low", "medium", "high", "xhigh", "max", "ultra"}:
            raise ValueError("unsupported Codex reasoning effort")
        self.workspace = workspace.resolve()
        self.log_dir = log_dir.resolve()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.executable = executable
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.timeout_seconds = timeout_seconds
        self.disable_nested_agents = disable_nested_agents

    def command(self, schema_path: Path, output_path: Path,
                reasoning_effort: str | None = None) -> list[str]:
        effort = reasoning_effort or self.reasoning_effort
        command = [
            self.executable, "exec", "--model", self.model,
            "--config", f'model_reasoning_effort="{effort}"',
        ]
        if self.disable_nested_agents:
            command.extend(["--disable", "multi_agent"])
        command.extend([
            "--ephemeral", "--sandbox", "read-only", "--cd", str(self.workspace),
            "--output-schema", str(schema_path),
            "--output-last-message", str(output_path), "-",
        ])
        return command

    def run(self, role: str, prompt: str, schema: dict[str, Any],
            reasoning_effort: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        digest = hashlib.sha256((role + prompt).encode()).hexdigest()[:10]
        invocation_id = f"{stamp}-{digest}-{uuid.uuid4().hex[:10]}"
        root = self.log_dir / invocation_id
        root.mkdir(parents=True, exist_ok=True)
        prompt_path = root / "prompt.txt"
        schema_path = root / "schema.json"
        output_path = root / "response.json"
        stderr_path = root / "stderr.txt"
        prompt_path.write_text(prompt)
        schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
        effort = reasoning_effort or self.reasoning_effort
        command = self.command(schema_path, output_path, effort)
        try:
            completed = subprocess.run(
                command, input=prompt, text=True, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, timeout=self.timeout_seconds, check=False)
            stderr_path.write_text(completed.stderr)
        except subprocess.TimeoutExpired as exc:
            stderr_path.write_text(f"Timed out after {self.timeout_seconds} seconds.\n")
            raise AgentError(f"{role} timed out; see {stderr_path}") from exc
        if completed.returncode != 0 or not output_path.exists():
            raise AgentError(f"{role} failed with exit code {completed.returncode}; see {stderr_path}")
        try:
            response = json.loads(output_path.read_text())
        except json.JSONDecodeError as exc:
            raise AgentError(f"{role} returned invalid JSON; see {output_path}") from exc
        metadata = {
            "role": role,
            "model": self.model,
            "reasoning_effort": effort,
            "nested_agents_disabled": self.disable_nested_agents,
            "invocation_id": invocation_id,
            "command": command[:-1],
            "response_path": str(output_path),
        }
        return response, metadata
