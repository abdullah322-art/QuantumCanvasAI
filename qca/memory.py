from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List, Tuple

from .config import settings
from .schemas import ChatMessage


class SlidingWindowMemory:
    """Session memory that forgets earliest turns when capacity is exceeded.

    A "turn" is a pair of (user, assistant) messages. We store raw messages,
    but purge from the start in pairs when we exceed `max_history_turns`.
    """

    def __init__(self, max_history_turns: int | None = None):
        self._turns: Dict[str, Deque[ChatMessage]] = defaultdict(deque)
        self.max_turns = max_history_turns or settings.max_history_turns

    def append(self, session_id: str, message: ChatMessage) -> None:
        self._turns[session_id].append(message)
        self._enforce_capacity(session_id)

    def get(self, session_id: str) -> List[ChatMessage]:
        return list(self._turns.get(session_id, deque()))

    def clear(self, session_id: str) -> None:
        self._turns.pop(session_id, None)

    def _enforce_capacity(self, session_id: str) -> None:
        dq = self._turns[session_id]
        # Count user+assistant pairs
        user_count = sum(1 for m in dq if m.role == "user")
        assistant_count = sum(1 for m in dq if m.role == "assistant")
        turns = min(user_count, assistant_count)
        while turns > self.max_turns and len(dq) >= 2:
            # Drop earliest two messages (ideally one user + one assistant)
            dq.popleft()
            if dq:
                dq.popleft()
            user_count = sum(1 for m in dq if m.role == "user")
            assistant_count = sum(1 for m in dq if m.role == "assistant")
            turns = min(user_count, assistant_count)


memory = SlidingWindowMemory()

