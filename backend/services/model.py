"""Carga del modelo entrenado e inferencia de la especie (PyTorch)."""

import json
from pathlib import Path

from .preprocess import prepare_image
from .species import get_species

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "animals.pt"
LABELS_PATH = MODEL_DIR / "labels.json"

_model = None
_labels = None
_device = None


def _load():
    """Cargar el modelo y las etiquetas una sola vez (perezoso)."""
    global _model, _labels, _device
    if _model is None:
        import torch
        from torch import nn
        from torchvision import models

        _labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Reconstruir la arquitectura y cargar los pesos entrenados
        model = models.mobilenet_v2()
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, len(_labels))
        model.load_state_dict(torch.load(MODEL_PATH, map_location=_device, weights_only=True))
        model.eval().to(_device)
        _model = model
    return _model, _labels, _device


def is_ready():
    """Indicar si existe un modelo entrenado en disco."""
    return MODEL_PATH.exists() and LABELS_PATH.exists()


def predict(raw_bytes):
    """Predecir la especie de una imagen y su confianza."""
    import torch

    model, labels, device = _load()
    tensor = prepare_image(raw_bytes).to(device)
    with torch.no_grad():
        # Convertir salidas en probabilidades
        probs = torch.softmax(model(tensor)[0], dim=0)
    best = int(probs.argmax())
    return {
        "species": get_species(labels[best]),
        "confidence": float(probs[best]),
    }
