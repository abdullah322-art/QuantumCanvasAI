from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator, Iterable, List

from ..schemas import ChatMessage


class Engine(ABC):
    @abstractmethod
    def complete(self, messages: List[ChatMessage], max_tokens: int, temperature: float) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream_complete(
        self, messages: List[ChatMessage], max_tokens: int, temperature: float
    ) -> Iterable[str] | Generator[str, None, None]:
        raise NotImplementedError

