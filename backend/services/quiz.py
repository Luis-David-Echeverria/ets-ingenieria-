"""Generacion y validacion de preguntas del quiz."""

import random

from .species import SPECIES


def make_question():
    """Armar una pregunta: un animal a adivinar y tres opciones."""
    answer = random.choice(SPECIES)
    # Elegir dos distractores distintos a la respuesta
    others = [s for s in SPECIES if s["id"] != answer["id"]]
    distractors = random.sample(others, 2)
    options = [answer, *distractors]
    random.shuffle(options)
    return {
        "imageId": answer["id"],
        "answerId": answer["id"],
        "options": options,
    }


def check_answer(image_id, choice_id):
    """Validar si la opcion elegida coincide con el animal mostrado."""
    return {"correct": image_id == choice_id, "answerId": image_id}
