import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings

INTENT_LABELS = ["ask", "summarize", "explain", "quiz", "compare", "checklist"]
DEFAULT_INTENT_MODEL_NAME = "bert-base-uncased"
DEFAULT_INTENT_TOKENIZER_NAME = "bert-base-uncased"


@dataclass
class IntentPrediction:
    label: str
    confidence: float


def predict_study_intent(text: str) -> IntentPrediction | None:
    model_dir = _get_model_dir()
    if not _has_trained_model(model_dir):
        return None

    try:
        tokenizer, model, labels, torch = _load_intent_bundle(model_dir)
    except ImportError:
        return None
    except Exception:
        return None

    with torch.no_grad():
        encoded = tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=96,
            return_tensors="pt",
        )
        outputs = model(**encoded)
        probabilities = torch.softmax(outputs.logits, dim=-1)[0]
        predicted_index = int(torch.argmax(probabilities).item())
        confidence = float(probabilities[predicted_index].item())

    if predicted_index >= len(labels):
        return None

    return IntentPrediction(label=labels[predicted_index], confidence=confidence)


def get_trained_intent_model_path() -> Path:
    return _get_model_dir()


def _get_model_dir() -> Path:
    settings = get_settings()
    return settings.intent_router_dir


def _has_trained_model(model_dir: Path) -> bool:
    base_files = [
        model_dir / "config.json",
        model_dir / "labels.json",
    ]
    weight_files = [
        model_dir / "model.safetensors",
        model_dir / "pytorch_model.bin",
    ]
    return all(path.exists() for path in base_files) and any(path.exists() for path in weight_files)


@lru_cache
def _load_intent_bundle(model_dir: Path):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
    model.eval()

    labels_path = model_dir / "labels.json"
    labels = json.loads(labels_path.read_text(encoding="utf-8"))
    return tokenizer, model, labels, torch
