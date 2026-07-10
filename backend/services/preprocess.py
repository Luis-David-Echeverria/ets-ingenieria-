"""Preprocesamiento de imagenes para el modelo (PyTorch)."""

import io

from PIL import Image
from torchvision import transforms

# Tamano de entrada esperado por MobileNetV2
IMG_SIZE = 224

# Redimensionar y normalizar igual que en el entrenamiento
_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def prepare_image(raw_bytes):
    """Convertir bytes de imagen en un tensor con dimension de lote."""
    # Abrir y forzar RGB (descarta canal alfa o escala de grises)
    image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    # Redimensionar, pasar a tensor y normalizar; agregar dimension de lote
    return _transform(image).unsqueeze(0)
