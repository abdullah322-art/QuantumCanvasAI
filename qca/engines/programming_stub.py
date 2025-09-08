from __future__ import annotations

import re
from typing import Iterable, List

from .base import Engine
from ..schemas import ChatMessage


SAFE_GUIDANCE = (
    "Always produce non-destructive, diff-style or explicit edits. "
    "Avoid deleting user code unless asked. Keep responses concise and actionable."
)


class ProgrammingStubEngine(Engine):
    """Deterministic programming assistant placeholder.

    Emphasizes diffs, step-by-step fixes, and safe transformations. This is
    a stand-in for a real code LLM. It does small analyses and deterministic
    suggestions to make local testing reliable.
    """

    def _summarize_issue(self, text: str) -> str:
        if not text:
            return "No code provided."
        if "error" in text.lower():
            return "Identified an error; propose a minimal fix."
        if re.search(r"\b(optimize|slow|performance)\b", text, re.I):
            return "Recommend performance optimizations."
        return "Provide implementation guidance with examples."

    def complete(self, messages: List[ChatMessage], max_tokens: int, temperature: float) -> str:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        summary = self._summarize_issue(last_user)
        suggestion = (
            f"{SAFE_GUIDANCE}\n\n"  # safety banner
            f"Summary: {summary}\n\n"
            "Proposed steps:\n"
            "1. Reproduce the issue.\n"
            "2. Add a failing test.\n"
            "3. Apply a minimal edit.\n"
            "4. Rerun tests and verify.\n"
        )
        return suggestion[: max_tokens * 4]

    def stream_complete(self, messages: List[ChatMessage], max_tokens: int, temperature: float) -> Iterable[str]:
        text = self.complete(messages, max_tokens, temperature)
        for token in text.split():
            yield token + " "

