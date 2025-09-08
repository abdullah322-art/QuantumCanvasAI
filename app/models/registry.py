from typing import Dict, List, Type
from .engines.mock import MockEngine, ProgrammerEngine

# Map model identifiers to engine classes and config
MODEL_REGISTRY: Dict[str, Dict] = {
    "QCA-4.9": {"engine": MockEngine, "tier": "free", "context": 8192},
    "QCA-5.0": {"engine": MockEngine, "tier": "free+", "context": 12000},
    "QCA-5.2": {"engine": ProgrammerEngine, "tier": "starter", "context": 16000},
    "QCA-5.4": {"engine": ProgrammerEngine, "tier": "starter+", "context": 20000},
    "QCA-5.6": {"engine": ProgrammerEngine, "tier": "pro", "context": 24000},
    "QCA-5.8": {"engine": ProgrammerEngine, "tier": "pro+", "context": 32000},
    "QCA-6.0": {"engine": ProgrammerEngine, "tier": "elite", "context": 48000},
    "QCA-6.2": {"engine": ProgrammerEngine, "tier": "elite+", "context": 64000},
    "QCA-6.5": {"engine": ProgrammerEngine, "tier": "ultra", "context": 96000},
    "QCA-6.8-SUPREME": {"engine": ProgrammerEngine, "tier": "supreme", "context": 128000},
}


def list_models() -> List[str]:
    return list(MODEL_REGISTRY.keys())


def get_engine(model: str):
    config = MODEL_REGISTRY.get(model)
    if not config:
        raise ValueError(f"Unknown model: {model}")
    return config["engine"](model_name=model, max_context_tokens=config["context"]) 
