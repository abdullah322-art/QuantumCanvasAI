from .base import Engine
from .programming_core import ProgrammingCore

ENGINES: dict[str, Engine] = {}

# Register ten versions with increasing capability tiers
VERSIONS = [
    ("QCA-4.9", "free"),
    ("QCA-5.1", "free-plus"),
    ("QCA-5.3", "starter"),
    ("QCA-5.5", "pro"),
    ("QCA-5.7", "pro+"),
    ("QCA-5.9", "team"),
    ("QCA-6.1", "business"),
    ("QCA-6.3", "business+"),
    ("QCA-6.5", "enterprise"),
    ("QCA-6.8-SUPREME", "ultra"),
]

for idx, (name, tier) in enumerate(VERSIONS):
    temperature = 0.1 + 0.02 * idx
    ENGINES[name] = ProgrammingCore(name=name, tier=tier, temperature=temperature)

__all__ = ["ENGINES", "VERSIONS"]
