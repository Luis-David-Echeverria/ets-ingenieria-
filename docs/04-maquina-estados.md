# Máquina de Estados

## Estados del Libro (navegación)

Refleja el recorrido lineal del cuento: la portada, la sección de identificar,
las preguntas del quiz y la contraportada.

```mermaid
stateDiagram-v2
    [*] --> Portada
    Portada --> Identificar : pasar página
    Identificar --> Invitacion : (misma vista, página derecha)
    Invitacion --> Quiz : pasar página
    Quiz --> Quiz : siguiente pregunta
    Quiz --> Contraportada : tras 6 preguntas
    Contraportada --> Portada : volver (reinicia el quiz)

    state Identificar {
        [*] --> Esperando
        Esperando --> Analizando : sube foto
        Analizando --> Reconocido : confianza >= 85%
        Analizando --> NoReconocido : confianza < 85%
        Reconocido --> Esperando : otra foto
        NoReconocido --> Esperando : otra foto
    }
```

## Estados de una pregunta del Quiz

```mermaid
stateDiagram-v2
    [*] --> SinResponder
    SinResponder --> Correcta : elige opción correcta
    SinResponder --> Incorrecta : elige opción incorrecta
    Correcta --> [*] : dice nombre + estrella
    Incorrecta --> [*] : dice nombre correcto
    note right of SinResponder
        Se muestran 3 nombres.
        Al responder se bloquean
        las opciones.
    end note
```

## Descripción de estados

| Estado | Descripción |
|--------|-------------|
| **Portada** | Libro cerrado; muestra la ilustración de portada. |
| **Identificar** | El niño sube fotos y recibe predicciones. |
| **Invitación** | Página que invita a jugar el quiz. |
| **Quiz** | Ronda de 6 preguntas de adivinanza (animales sin repetir). |
| **Contraportada** | Muestra el puntaje en estrellas y los créditos. |
| **Analizando** | El modelo está procesando la imagen. |
| **Reconocido / NoReconocido** | Resultado según el umbral de confianza (85%). |
