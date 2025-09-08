from __future__ import annotations

import textwrap
from typing import Iterable, List

from .base import Engine
from ..schemas import ChatMessage


class GeneralStubEngine(Engine):
    """Deterministic placeholder engine for general dialogue.

    This engine is safe for testing and avoids hallucinations by mirroring
    context and offering a concise, helpful reply, with deterministic output.
    Replace this with your real model integration.
    """

    def complete(self, messages: List[ChatMessage], max_tokens: int, temperature: float) -> str:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "" )
        reply = textwrap.dedent(
            f"""
            I am QCA. Here's a concise answer based on your last request:
            {last_user.strip()}
            """
        ).strip()
        return reply[: max_tokens * 4]

    def stream_complete(self, messages: List[ChatMessage], max_tokens: int, temperature: float) -> Iterable[str]:
        text = self.complete(messages, max_tokens, temperature)
        for chunk in text.split():
            yield chunk + " "

