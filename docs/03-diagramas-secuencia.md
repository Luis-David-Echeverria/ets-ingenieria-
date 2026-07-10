# Diagramas de Secuencia

## Secuencia 1: Identificar un animal por foto

Muestra el flujo desde que el niño sube una foto hasta que escucha el nombre.

```mermaid
sequenceDiagram
    actor Nino as Niño
    participant UI as Frontend (Libro)
    participant API as Backend (FastAPI)
    participant Pre as Preprocessor
    participant Model as AnimalClassifier

    Nino->>UI: Sube una foto
    UI->>UI: Muestra vista previa
    UI->>API: POST /predict (imagen)
    API->>Pre: prepare_image(bytes)
    Pre->>Pre: Redimensiona 224x224 + normaliza
    Pre-->>API: tensor
    API->>Model: forward(tensor)
    Model-->>API: probabilidades por clase
    API->>API: argmax + softmax
    API-->>UI: {species, confidence}
    alt confianza >= 85%
        UI->>UI: Muestra ícono + nombre + %
        UI->>Nino: Dice el nombre en voz alta (TTS)
    else confianza < 85%
        UI->>Nino: "No pude reconocer al animal"
    end
```

## Secuencia 2: Responder una pregunta del quiz

Muestra el flujo de una ronda de adivinanza.

```mermaid
sequenceDiagram
    actor Nino as Niño
    participant UI as Frontend (Libro)
    participant API as Backend (FastAPI)
    participant Quiz as QuizService

    UI->>API: GET /quiz
    API->>Quiz: make_question()
    Quiz->>Quiz: Elige animal + 2 distractores
    Quiz-->>API: {imageId, answerId, options}
    API-->>UI: pregunta
    UI->>Nino: Muestra ícono del animal + 3 nombres

    Nino->>UI: Elige un nombre
    UI->>API: POST /quiz/check {imageId, choiceId}
    API->>Quiz: check_answer(imageId, choiceId)
    Quiz-->>API: {correct, answerId}
    API-->>UI: resultado
    UI->>UI: Marca verde/rojo + suma estrella
    UI->>Nino: Dice el nombre en voz alta

    Note over UI,Nino: Al terminar las 6 preguntas,<br/>el libro se cierra y muestra las estrellas
```
