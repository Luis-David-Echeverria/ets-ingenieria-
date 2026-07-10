# Metricas de evaluacion del modelo

**Modelo:** MobileNetV2 (transfer learning)  
**Conjunto de validacion:** 5235 imagenes  
**Accuracy global:** 0.9463 (94.63%)

| Especie | Precision | Sensibilidad (recall) | Especificidad | F1 |
|---------|-----------|-----------------------|---------------|-----|
| Perro | 0.920 | 0.968 | 0.981 | 0.943 |
| Caballo | 0.957 | 0.928 | 0.995 | 0.942 |
| Elefante | 0.953 | 0.964 | 0.997 | 0.958 |
| Mariposa | 0.968 | 0.942 | 0.998 | 0.955 |
| Gallina | 0.943 | 0.965 | 0.992 | 0.954 |
| Gato | 0.993 | 0.859 | 1.000 | 0.921 |
| Vaca | 0.935 | 0.848 | 0.995 | 0.889 |
| Oveja | 0.863 | 0.944 | 0.988 | 0.902 |
| Araña | 0.977 | 0.987 | 0.994 | 0.982 |
| Ardilla | 0.973 | 0.939 | 0.998 | 0.956 |
| **Promedio** | **0.948** | **0.934** | **0.994** | **0.940** |

## Matriz de confusion

| real \ pred | Perro | Caballo | Elefante | Mariposa | Gallina | Gato | Vaca | Oveja | Araña | Ardilla |
|---|---|---|---|---|---|---|---|---|---|---|
| **Perro** | 941 | 5 | 0 | 0 | 8 | 1 | 4 | 10 | 3 | 0 |
| **Caballo** | 15 | 488 | 5 | 0 | 0 | 0 | 11 | 6 | 1 | 0 |
| **Elefante** | 2 | 2 | 265 | 1 | 0 | 0 | 1 | 4 | 0 | 0 |
| **Mariposa** | 3 | 0 | 1 | 358 | 4 | 0 | 0 | 0 | 13 | 1 |
| **Gallina** | 11 | 1 | 0 | 2 | 583 | 0 | 1 | 3 | 1 | 2 |
| **Gato** | 33 | 0 | 0 | 1 | 3 | 267 | 0 | 3 | 0 | 4 |
| **Vaca** | 8 | 11 | 4 | 1 | 1 | 0 | 317 | 32 | 0 | 0 |
| **Oveja** | 5 | 3 | 3 | 0 | 6 | 0 | 5 | 372 | 0 | 0 |
| **Araña** | 1 | 0 | 0 | 7 | 2 | 0 | 0 | 0 | 1008 | 3 |
| **Ardilla** | 4 | 0 | 0 | 0 | 11 | 1 | 0 | 1 | 6 | 355 |