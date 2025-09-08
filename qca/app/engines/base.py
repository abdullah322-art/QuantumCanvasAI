from abc import ABC, abstractmethod
from typing import Dict, Any, List

class EngineResponse(Dict[str, Any]):
    pass

class Engine(ABC):
    name: str
    tier: str
    temperature: float

    def __init__(self, name: str, tier: str, temperature: float = 0.2):
        self.name = name
        self.tier = tier
        self.temperature = temperature

    @abstractmethod
    def complete(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] | None = None) -> EngineResponse:
        ...
