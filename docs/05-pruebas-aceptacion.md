# Pruebas de Aceptación

Casos de prueba ejecutados sobre el sistema para validar la funcionalidad,
usabilidad y el rendimiento del modelo.

## Pruebas funcionales

| ID | Caso de prueba | Pasos | Resultado esperado | Estado |
|----|----------------|-------|--------------------|--------|
| PA-01 | Identificar un perro | Subir foto de perro | Predice "Perro" con alta confianza y lo dice en voz alta | Pasó (99.8%) |
| PA-02 | Identificar un elefante | Subir foto de elefante | Predice "Elefante" | Pasó (99.9%) |
| PA-03 | Identificar una araña | Subir foto de araña | Predice "Araña" | Pasó (99.9%) |
| PA-04 | Umbral de confianza | Subir imagen ambigua / no-animal | Muestra "No pude reconocer" si < 85% | Pasó |
| PA-05 | Reproducción de voz | Identificar cualquier animal | El sistema dice el nombre (voz femenina, español) | Pasó |
| PA-06 | Generar pregunta de quiz | Entrar al quiz | Muestra un animal y 3 opciones (incluye la correcta) | Pasó |
| PA-07 | Responder correctamente | Elegir el nombre correcto | Marca verde, suma estrella, dice el nombre | Pasó |
| PA-08 | Responder incorrectamente | Elegir nombre incorrecto | Marca rojo, revela el correcto | Pasó |
| PA-09 | Animales sin repetir | Jugar las 6 preguntas | Ningún animal aparece dos veces | Pasó |
| PA-10 | Puntaje final | Terminar el quiz | Muestra estrellas según aciertos (X de 6) | Pasó |
| PA-11 | Reinicio del quiz | Volver a la portada y reabrir | Preguntas nuevas y aleatorias | Pasó |

## Pruebas de validación (robustez)

| ID | Caso de prueba | Entrada | Resultado esperado | Estado |
|----|----------------|---------|--------------------|--------|
| PV-01 | Archivo no-imagen (cliente) | Arrastrar un audio/texto | Rechaza y avisa "Eso no es una foto" | Pasó |
| PV-02 | Archivo no-imagen (servidor) | POST /predict con .txt | HTTP 400 "El archivo debe ser una imagen" | Pasó |
| PV-03 | Imagen demasiado grande | Foto > 10 MB | Rechaza (cliente y servidor, HTTP 413) | Pasó |
| PV-04 | Imagen corrupta | Bytes que no abren como imagen | HTTP 400 "no es una imagen valida" | Pasó |
| PV-05 | Especie desconocida en quiz | POST /quiz/check con id inexistente | HTTP 400 "Especie desconocida" | Pasó |
| PV-06 | Fallo del servidor | Backend caído durante identificar | Muestra "No pude analizar la foto" sin colgarse | Pasó |

## Pruebas de usabilidad

| ID | Aspecto | Criterio | Estado |
|----|---------|----------|--------|
| PU-01 | Interfaz amigable | Botones grandes, colores cálidos, tipografía de crayón | Pasó |
| PU-02 | Navegación intuitiva | Metáfora de libro (pasar páginas) | Pasó |
| PU-03 | Retroalimentación clara | Verde/rojo + voz al responder | Pasó |
| PU-04 | Accesibilidad auditiva | Nombres en voz alta para asociación | Pasó |

## Pruebas de rendimiento del modelo

| Métrica | Valor | Requisito PDF | Estado |
|---------|-------|---------------|--------|
| Accuracy (validación) | **94.63%** | Buena eficiencia | Supera |
| Precisión (promedio) | **94.8%** | Requerida | Sí |
| Sensibilidad (recall) | **93.4%** | Requerida | Sí |
| Especificidad | **99.4%** | Requerida | Sí |
| Tiempo de predicción | < 2 s | Fluido | Sí |

> El detalle por especie y la matriz de confusión están en [metricas.md](metricas.md).

## Condiciones de la prueba

- **Conjunto de validación:** 5,235 imágenes (20% del dataset, no vistas en entrenamiento).
- **Dataset:** Animals-10 (~26,000 imágenes, 10 especies).
- **Hardware:** GPU NVIDIA RTX 4060 Ti.
- **Modelo:** MobileNetV2 con transfer learning (3 épocas).
