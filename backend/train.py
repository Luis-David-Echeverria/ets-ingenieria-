"""Entrenamiento del clasificador de animales con transfer learning (MobileNetV2).

Usa PyTorch + torchvision y la GPU si esta disponible.
Uso: python train.py
Lee el dataset de ../archive/raw-img (carpetas en italiano), entrena y guarda
el modelo en models/animals.pt junto con models/labels.json.
"""

import json
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms

from services.species import FOLDER_TO_ID

# Rutas del dataset y de salida
DATA_DIR = Path(__file__).resolve().parent.parent / "archive" / "raw-img"
MODEL_DIR = Path(__file__).resolve().parent / "models"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 3

# Usar la GPU si esta disponible
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Normalizacion estandar de ImageNet (la que espera MobileNetV2)
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]


def build_loaders():
    """Cargar el dataset y dividirlo en entrenamiento y validacion."""
    # Aumento de datos para entrenar (generalizar mejor)
    train_tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(12),
        transforms.ColorJitter(0.1, 0.1, 0.1),
        transforms.ToTensor(),
        transforms.Normalize(NORM_MEAN, NORM_STD),
    ])
    # Solo redimensionar y normalizar para validar
    val_tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(NORM_MEAN, NORM_STD),
    ])

    # Dos vistas del mismo dataset, cada una con su transformacion
    train_full = datasets.ImageFolder(DATA_DIR, transform=train_tf)
    val_full = datasets.ImageFolder(DATA_DIR, transform=val_tf)

    # Repartir los mismos indices en entrenamiento y validacion
    n_val = int(len(train_full) * 0.2)
    n_train = len(train_full) - n_val
    generator = torch.Generator().manual_seed(123)
    train_idx, val_idx = random_split(range(len(train_full)), [n_train, n_val], generator=generator)

    train_set = torch.utils.data.Subset(train_full, list(train_idx))
    val_set = torch.utils.data.Subset(val_full, list(val_idx))

    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_set, batch_size=BATCH_SIZE, num_workers=4)
    return train_loader, val_loader, train_full.classes


def build_model(num_classes):
    """Construir el modelo: base MobileNetV2 preentrenada + cabeza nueva."""
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    # Congelar la base para aprovechar lo que ya aprendio
    for param in model.features.parameters():
        param.requires_grad = False
    # Reemplazar el clasificador por uno de 10 clases
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model.to(DEVICE)


def run_epoch(model, loader, criterion, optimizer=None):
    """Ejecutar una epoca de entrenamiento o validacion."""
    training = optimizer is not None
    model.train() if training else model.eval()
    total, correct, loss_sum = 0, 0, 0.0

    with torch.set_grad_enabled(training):
        for images, targets in loader:
            images, targets = images.to(DEVICE), targets.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, targets)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            loss_sum += loss.item() * images.size(0)
            correct += (outputs.argmax(1) == targets).sum().item()
            total += images.size(0)

    return loss_sum / total, correct / total


def main():
    print("Dispositivo:", DEVICE)
    train_loader, val_loader, folder_names = build_loaders()

    # Traducir los nombres de carpeta (italiano) a ids en espanol
    labels = [FOLDER_TO_ID[name] for name in folder_names]

    model = build_model(len(labels))
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.classifier.parameters(), lr=1e-3)

    for epoch in range(1, EPOCHS + 1):
        tr_loss, tr_acc = run_epoch(model, train_loader, criterion, optimizer)
        va_loss, va_acc = run_epoch(model, val_loader, criterion)
        print(
            f"Epoca {epoch}/{EPOCHS} - "
            f"train acc {tr_acc:.3f} - val acc {va_acc:.3f}"
        )

    # Guardar el modelo y las etiquetas
    MODEL_DIR.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_DIR / "animals.pt")
    (MODEL_DIR / "labels.json").write_text(json.dumps(labels), encoding="utf-8")
    print("Modelo guardado en", MODEL_DIR)


if __name__ == "__main__":
    main()
