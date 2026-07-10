"""Evaluacion del modelo: accuracy, precision, sensibilidad y especificidad.

Uso: python evaluate.py
Reconstruye el conjunto de validacion (mismo split del entrenamiento) y
calcula las metricas de clasificacion sobre el modelo ya entrenado.
Guarda el reporte y la matriz de confusion en ../docs/.
"""

import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset, random_split
from torchvision import datasets, models, transforms
from sklearn.metrics import confusion_matrix, classification_report

from services.species import FOLDER_TO_ID, get_species

DATA_DIR = Path(__file__).resolve().parent.parent / "archive" / "raw-img"
MODEL_DIR = Path(__file__).resolve().parent / "models"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
IMG_SIZE = 224
BATCH_SIZE = 32
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_val_loader():
    """Reconstruir el conjunto de validacion con el mismo split del entrenamiento."""
    tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    full = datasets.ImageFolder(DATA_DIR, transform=tf)
    n_val = int(len(full) * 0.2)
    n_train = len(full) - n_val
    _, val_idx = random_split(
        range(len(full)), [n_train, n_val], generator=torch.Generator().manual_seed(123)
    )
    val_set = Subset(full, list(val_idx))
    loader = DataLoader(val_set, batch_size=BATCH_SIZE, num_workers=4)
    return loader, full.classes


def load_model(num_classes):
    """Cargar el modelo entrenado."""
    model = models.mobilenet_v2()
    in_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_features, num_classes)
    model.load_state_dict(torch.load(MODEL_DIR / "animals.pt", map_location=DEVICE, weights_only=True))
    return model.eval().to(DEVICE)


def specificity_per_class(cm):
    """Calcular la especificidad de cada clase a partir de la matriz de confusion."""
    specs = []
    total = cm.sum()
    for i in range(len(cm)):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        tn = total - tp - fp - fn
        specs.append(tn / (tn + fp) if (tn + fp) > 0 else 0.0)
    return specs


def main():
    loader, folder_names = build_val_loader()
    labels_es = [FOLDER_TO_ID[name] for name in folder_names]
    names = [get_species(i)["name"] for i in labels_es]

    model = load_model(len(labels_es))

    # Recolectar predicciones y verdaderos
    y_true, y_pred = [], []
    with torch.no_grad():
        for images, targets in loader:
            outputs = model(images.to(DEVICE))
            y_pred.extend(outputs.argmax(1).cpu().numpy())
            y_true.extend(targets.numpy())

    y_true, y_pred = np.array(y_true), np.array(y_pred)
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=names, output_dict=True)
    specs = specificity_per_class(cm)

    # Armar el reporte de metricas
    accuracy = report["accuracy"]
    lines = []
    lines.append("# Metricas de evaluacion del modelo\n")
    lines.append(f"**Modelo:** MobileNetV2 (transfer learning)  ")
    lines.append(f"**Conjunto de validacion:** {len(y_true)} imagenes  ")
    lines.append(f"**Accuracy global:** {accuracy:.4f} ({accuracy * 100:.2f}%)\n")
    lines.append("| Especie | Precision | Sensibilidad (recall) | Especificidad | F1 |")
    lines.append("|---------|-----------|-----------------------|---------------|-----|")
    for i, name in enumerate(names):
        r = report[name]
        lines.append(
            f"| {name} | {r['precision']:.3f} | {r['recall']:.3f} | "
            f"{specs[i]:.3f} | {r['f1-score']:.3f} |"
        )
    macro = report["macro avg"]
    lines.append(
        f"| **Promedio** | **{macro['precision']:.3f}** | **{macro['recall']:.3f}** | "
        f"**{np.mean(specs):.3f}** | **{macro['f1-score']:.3f}** |\n"
    )

    # Matriz de confusion en texto
    lines.append("## Matriz de confusion\n")
    header = "| real \\ pred | " + " | ".join(names) + " |"
    lines.append(header)
    lines.append("|" + "---|" * (len(names) + 1))
    for i, name in enumerate(names):
        row = f"| **{name}** | " + " | ".join(str(int(v)) for v in cm[i]) + " |"
        lines.append(row)

    DOCS_DIR.mkdir(exist_ok=True)
    out = DOCS_DIR / "metricas.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    # Guardar la matriz de confusion como heatmap
    guardar_heatmap(cm, names)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Reporte guardado en {out}")


def guardar_heatmap(cm, names):
    """Dibujar la matriz de confusion como imagen (heatmap)."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(cm, cmap="YlOrBr")
    ax.set_xticks(range(len(names)), labels=names, rotation=45, ha="right")
    ax.set_yticks(range(len(names)), labels=names)
    ax.set_xlabel("Predicho")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de confusión — validación")

    # Escribir el numero en cada celda
    umbral = cm.max() / 2
    for i in range(len(names)):
        for j in range(len(names)):
            color = "white" if cm[i, j] > umbral else "black"
            ax.text(j, i, int(cm[i, j]), ha="center", va="center", color=color, fontsize=8)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(DOCS_DIR / "imagenes" / "matriz-confusion.png", dpi=150)
    plt.close(fig)
    print("Generado matriz-confusion.png")


if __name__ == "__main__":
    main()
