from __future__ import annotations
from typing import List, Dict, Any

class BaseEngine:
    def __init__(self, model_name: str, max_context_tokens: int = 8192):
        self.model_name = model_name
        self.max_context_tokens = max_context_tokens

    def generate(self, messages: List[Dict[str, str]], system_prompt: str | None = None) -> Dict[str, Any]:
        raise NotImplementedError


class MockEngine(BaseEngine):
    def generate(self, messages: List[Dict[str, str]], system_prompt: str | None = None) -> Dict[str, Any]:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        reply = f"[QCA mock:{self.model_name}] You said: {last_user[:500]}"
        return {"role": "assistant", "content": reply}


class ProgrammerEngine(BaseEngine):
    def generate(self, messages: List[Dict[str, str]], system_prompt: str | None = None) -> Dict[str, Any]:
        # A deterministic, formatting‑aware programmer style mock
        user_parts = [m["content"] for m in messages if m["role"] == "user"]
        prompt = user_parts[-1] if user_parts else ""
        guidance = (
            "Follow best practices, avoid destructive actions, and never delete user code. "
            "Provide minimal, runnable examples with language fenced blocks."
        )
        content = (
            f"QCA Programmer Mode ({self.model_name})\n\n"
            f"Key guidance: {guidance}\n\n"
            f"Response to prompt:\n{prompt[:1000]}\n\n"
            "If you asked for code, here is a template to start:\n\n"
            "```python\n# Your Python starter template\nif __name__ == '__main__':\n    print('Hello from QCA Programmer Mode')\n```\n"
        )
        return {"role": "assistant", "content": content}
