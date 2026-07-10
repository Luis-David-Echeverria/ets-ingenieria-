# Diagrama de Casos de Uso

Actores del sistema: el **Niño** (usuario principal) y el **Profesor** (guía/supervisor).
Ambos pueden usar todas las funciones; el profesor típicamente acompaña.

```mermaid
graph LR
    Nino([Niño])
    Profesor([Profesor])

    subgraph Sistema["El Gran Libro de los Animales"]
        UC1((Abrir el libro))
        UC2((Identificar animal<br/>por foto))
        UC3((Escuchar el nombre<br/>en voz alta))
        UC4((Jugar al quiz))
        UC5((Responder pregunta<br/>de opción múltiple))
        UC6((Ver resultado<br/>y estrellas))
        UC7((Ver créditos<br/>del autor))
    end

    Nino --- UC1
    Nino --- UC2
    Nino --- UC4
    Nino --- UC5
    Nino --- UC6
    Profesor --- UC2
    Profesor --- UC4
    Profesor --- UC7

    UC2 -.->|include| UC3
    UC5 -.->|include| UC3
    UC4 -.->|include| UC5
    UC5 -.->|extend| UC6
```

## Descripción de casos de uso

| ID | Caso de uso | Actor | Descripción |
|----|-------------|-------|-------------|
| CU-01 | Abrir el libro | Niño | Pasa la portada para entrar al cuento. |
| CU-02 | Identificar animal por foto | Niño, Profesor | Sube una foto; el modelo predice la especie. |
| CU-03 | Escuchar el nombre | Niño | El sistema dice el nombre del animal en voz alta (TTS). |
| CU-04 | Jugar al quiz | Niño, Profesor | Inicia la ronda de preguntas de adivinanza. |
| CU-05 | Responder pregunta | Niño | Elige el nombre correcto entre 3 opciones. |
| CU-06 | Ver resultado y estrellas | Niño | Al terminar, ve su puntaje en estrellas. |
| CU-07 | Ver créditos del autor | Profesor | Consulta los datos del alumno (verificación de autoría). |

**Relaciones:**
- *include*: Identificar y Responder **siempre** dicen el nombre en voz alta.
- *extend*: al responder la última pregunta, se **extiende** hacia el resultado.
