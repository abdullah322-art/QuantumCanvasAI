from .base import Engine, EngineResponse
from typing import Dict, Any, List

class ProgrammingCore(Engine):
    def complete(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] | None = None) -> EngineResponse:
        prompt = "\n".join([f"{m[role]}: {m[content]}" for m in messages[-8:]])
        # Placeholder deterministic pseudo-completion to avoid hallucination in stub.
        code_hint = "If asking for code, provide clear, runnable examples with tests."
        return EngineResponse({
            "model": self.name,
            "tier": self.tier,
            "completion": f"[QCA ProgrammingCore] Analyzed {len(messages)} messages. {code_hint}",
            "safety": {"disallowed": []},
        })
