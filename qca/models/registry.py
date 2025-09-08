from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..schemas import ModelInfo


@dataclass
class ModelSpec:
    model_info: ModelInfo
    engine: str  # engine key used by engine router


def _build_models() -> Dict[str, ModelSpec]:
    models: Dict[str, ModelSpec] = {}

    versions = [
        ("qca-4.9", "QCA 4.9", "Entry model with solid reasoning and coding."),
        ("qca-5.1", "QCA 5.1", "Improved planning and tool-use scaffolding."),
        ("qca-5.3", "QCA 5.3", "Longer context and safer refactors."),
        ("qca-5.5", "QCA 5.5", "Faster responses with better determinism."),
        ("qca-5.7", "QCA 5.7", "Enhanced multilingual programming support."),
        ("qca-5.9", "QCA 5.9", "Reliable streaming and extended tools."),
        ("qca-6.1", "QCA 6.1", "Advanced program synthesis and tests."),
        ("qca-6.3", "QCA 6.3", "Refined agentic planning, low hallucination."),
        ("qca-6.5", "QCA 6.5", "Large context, precise code diffs."),
        ("qca-6.8-supereme", "QCA 6.8 SUPEREME", "Top tier model for all tasks."),
    ]

    for i, (mid, display, desc) in enumerate(versions):
        tier = "free" if i < 3 else ("pro" if i < 7 else "enterprise")
        models[mid] = ModelSpec(
            model_info=ModelInfo(
                id=mid,
                version=mid.split("-", 1)[1],
                display_name=display,
                description=desc,
                context_window=128000 if i >= 8 else (64000 if i >= 5 else 32000),
                max_output_tokens=8192 if i >= 8 else 4096,
                pricing_tier=tier,
            ),
            engine="programming" if i >= 2 else "general",
        )

    return models


MODEL_SPECS: Dict[str, ModelSpec] = _build_models()


def list_models() -> List[ModelInfo]:
    return [spec.model_info for spec in MODEL_SPECS.values()]


def get_model_spec(model_id: str) -> ModelSpec:
    spec = MODEL_SPECS.get(model_id)
    if not spec:
        raise KeyError(f"Unknown model id: {model_id}")
    return spec

