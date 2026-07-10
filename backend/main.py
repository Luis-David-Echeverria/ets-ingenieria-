"""API del clasificador de animales para ninos."""

import io
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field

from services import model, quiz
from services.species import BY_ID, SPECIES

# Carpeta del build del frontend (si existe, el backend lo sirve)
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

# Tamano maximo de imagen aceptado (10 MB)
MAX_IMAGE_BYTES = 10 * 1024 * 1024


def is_valid_image(data):
    """Verificar que los bytes correspondan a una imagen abrible."""
    try:
        Image.open(io.BytesIO(data)).verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False


app = FastAPI(title="El Gran Libro de los Animales")

# Permitir llamadas desde el frontend (local en cualquier puerto)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)


class CheckBody(BaseModel):
    imageId: str = Field(min_length=1)
    choiceId: str = Field(min_length=1)


@app.get("/species")
def list_species():
    """Listar las especies que el sistema reconoce."""
    return SPECIES


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Clasificar la imagen recibida y devolver la especie."""
    if not model.is_ready():
        raise HTTPException(503, "El modelo aun no esta entrenado")

    # Validar que el archivo sea una imagen
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "El archivo debe ser una imagen")

    data = await file.read()

    # Validar que no venga vacio y no exceda el tamano maximo
    if not data:
        raise HTTPException(400, "El archivo esta vacio")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "La imagen es demasiado grande (maximo 10 MB)")

    # Validar que los bytes sean una imagen abrible
    if not is_valid_image(data):
        raise HTTPException(400, "El archivo no es una imagen valida")

    return model.predict(data)


@app.get("/quiz")
def get_quiz():
    """Entregar una pregunta aleatoria del quiz."""
    return quiz.make_question()


@app.post("/quiz/check")
def check_quiz(body: CheckBody):
    """Validar la respuesta elegida en el quiz."""
    # Validar que los ids correspondan a especies conocidas
    if body.imageId not in BY_ID or body.choiceId not in BY_ID:
        raise HTTPException(400, "Especie desconocida")
    return quiz.check_answer(body.imageId, body.choiceId)


@app.get("/health")
def health():
    """Estado del servicio y si el modelo esta listo."""
    return {"ok": True, "model_ready": model.is_ready()}


# Servir el build del frontend si esta presente (montar al final)
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
