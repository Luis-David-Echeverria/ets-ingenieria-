# Guía de estudio para la evaluación del ETS

**Evaluación:** lunes 13 de julio, 11:00 am, sala 4206.
**Qué evalúan:** (1) la aplicación funcionando completa, (2) la documentación, y
(3) conocimientos de la materia aplicados a tu proyecto.

Esta guía te prepara para los tres puntos. Léela varias veces y asegúrate de poder
**explicar con tus palabras** cada concepto, no solo memorizarlo.

---

## 1. Resumen de tu proyecto (para explicarlo en 1 minuto)

> "Es un sistema web educativo para niños de primaria que identifica especies de
> animales a partir de fotos, usando una red neuronal (deep learning). Tiene dos
> modos: uno para identificar un animal subiendo su foto (y lo dice en voz alta), y
> un quiz donde el niño adivina el nombre del animal. El modelo reconoce 10 especies
> con un 94.6% de exactitud."

**Arquitectura en una frase:** frontend en React (la interfaz tipo libro de cuento),
que se comunica por una API REST (FastAPI en Python) con un modelo de inteligencia
artificial (MobileNetV2) que hace la clasificación.

---

## 2. Transfer Learning (lo más importante que van a preguntar)

### ¿Qué es?

**Transfer learning (aprendizaje por transferencia)** es reutilizar una red neuronal
que **ya fue entrenada** para una tarea, y adaptarla a una tarea nueva y parecida.

En vez de entrenar una red desde cero (que necesitaría millones de imágenes y mucho
tiempo), tomas una red que **ya aprendió a "ver"** y solo le enseñas lo específico de
tu problema.

### La analogía fácil (para explicarlo)

> "Es como una persona que ya sabe dibujar. Si le pides que aprenda a dibujar un animal
> nuevo, no tiene que aprender desde cero qué es una línea, una forma o una sombra; ya
> sabe lo básico y solo aprende los detalles del animal nuevo. La red preentrenada ya
> sabe reconocer bordes, texturas y formas; yo solo le enseño a distinguir mis 10
> animales."

### ¿Por qué funciona?

Una red entrenada con millones de imágenes (como **ImageNet**, que tiene 1.2 millones
de imágenes de 1000 categorías) aprende en sus **primeras capas** a detectar cosas
generales: bordes, colores, texturas, formas. Esas cosas sirven para **cualquier**
imagen. Solo las **últimas capas** son específicas de la tarea. Entonces:

- **Congelamos** las primeras capas (conservan lo que ya saben).
- **Reemplazamos y entrenamos** solo la última capa para nuestras 10 clases.

### Cómo lo aplicaste TÚ en el proyecto

1. Tomaste **MobileNetV2**, ya entrenada en ImageNet.
2. **Congelaste** su base (`features`) para no perder lo que sabe (`requires_grad = False`).
3. **Reemplazaste** la última capa (el "clasificador") por una nueva de **10 salidas**
   (una por especie).
4. Entrenaste **solo esa última capa** con tu dataset de animales (3 épocas).

Por eso entrenó rapidísimo (pocos minutos) y con alta precisión: la red ya sabía "ver",
solo aprendió a nombrar tus 10 animales.

### Frase clave para el examen

> "Usé transfer learning con MobileNetV2 preentrenada en ImageNet: congelé la base
> convolucional y entrené solo una nueva capa clasificadora de 10 clases. Esto me dio
> 94.6% de exactitud entrenando pocos minutos, en lugar de necesitar millones de
> imágenes y días de entrenamiento."

---

## 3. Conceptos de deep learning que pueden preguntar

### ¿Qué es una red neuronal convolucional (CNN)?

Es el tipo de red que se usa para imágenes. Aplica **filtros (convoluciones)** que
recorren la imagen detectando patrones: primero bordes simples, luego formas, luego
objetos completos. MobileNetV2 es una CNN.

### ¿Qué es MobileNetV2?

Una arquitectura de CNN **ligera y eficiente**, diseñada para funcionar rápido incluso
en dispositivos móviles. La elegí porque es rápida de entrenar y de hacer inferencia, y
da buena precisión. Alternativas más pesadas: ResNet50, EfficientNet.

### ¿Qué es una época (epoch)?

Una época es una pasada completa por **todo** el conjunto de entrenamiento. Entrené 3
épocas. Más épocas puede mejorar el modelo pero también puede causar sobreajuste.

### ¿Qué es el sobreajuste (overfitting)?

Cuando el modelo **memoriza** los datos de entrenamiento en vez de **aprender a
generalizar**. Se detecta cuando acierta mucho en entrenamiento pero mal en datos
nuevos. Cómo lo evité:
- **Data augmentation** (volteos, rotaciones, cambios de color): crea variaciones de las
  imágenes para que el modelo no memorice.
- **Dropout** (0.3): "apaga" aleatoriamente neuronas durante el entrenamiento para que
  no dependa de unas pocas.
- **Congelar la base**: al entrenar menos parámetros, hay menos riesgo de memorizar.

### ¿Qué es el preprocesamiento?

Preparar las imágenes antes de dárselas al modelo. En tu caso:
1. **Redimensionar** a 224×224 píxeles (tamaño que espera MobileNetV2).
2. **Normalizar** los valores de los píxeles (con la media y desviación de ImageNet),
   para que estén en el rango que el modelo aprendió.

---

## 4. Las métricas (te van a preguntar qué significan)

Todas se calculan comparando lo que el modelo predijo contra la respuesta correcta.
Se basan en 4 conteos: **VP** (verdaderos positivos), **VN** (verdaderos negativos),
**FP** (falsos positivos), **FN** (falsos negativos).

| Métrica | Qué mide | Fórmula | Tu resultado |
|---------|----------|---------|--------------|
| **Accuracy (exactitud)** | De todo, cuánto acertó | (VP+VN) / total | 94.63% |
| **Precisión** | De lo que dijo "es X", cuánto era X de verdad | VP / (VP+FP) | 94.8% |
| **Sensibilidad (recall)** | De los que SÍ eran X, cuántos detectó | VP / (VP+FN) | 93.4% |
| **Especificidad** | De los que NO eran X, cuántos descartó bien | VN / (VN+FP) | 99.4% |

### Cómo explicar cada una (con el ejemplo de "perro")

- **Precisión:** "De todas las veces que el modelo dijo *perro*, ¿cuántas eran perro de
  verdad? Alta precisión = pocos falsos positivos."
- **Sensibilidad (recall):** "De todos los perros que había, ¿cuántos reconoció como
  perro? Alta sensibilidad = pocos perros se le escaparon."
- **Especificidad:** "De todos los animales que NO eran perro, ¿cuántos correctamente NO
  clasificó como perro?"
- **F1:** promedio balanceado entre precisión y sensibilidad (por si preguntan).

### ¿Qué es la matriz de confusión?

Una tabla que muestra, para cada clase real, qué predijo el modelo. La **diagonal** son
los aciertos; fuera de la diagonal, los errores. En tu proyecto, por ejemplo, la vaca a
veces se confundió con la oveja (32 casos) porque son animales de granja parecidos. Es
útil para ver **qué clases se confunden entre sí**.

### ¿Qué es el conjunto de validación?

Dividiste el dataset: **80% para entrenar** y **20% para validar**. El modelo NUNCA vio
las imágenes de validación durante el entrenamiento, así que sirven para medir si de
verdad **generaliza** (no solo memoriza). Tus 94.6% son sobre esas 5,235 imágenes que
no vio.

---

## 5. Sobre el dataset

- **Nombre:** Animals-10 (de Kaggle).
- **Tamaño:** ~26,000 imágenes, 10 especies.
- **Clases:** perro, gato, caballo, elefante, mariposa, gallina, vaca, oveja, araña, ardilla.
- **Detalle:** las carpetas venían en italiano (cane, gatto, cavallo...) y las mapeé a español.

---

## 6. Arquitectura del sistema (te pueden preguntar cómo se comunican las partes)

```
NAVEGADOR (niño)                SERVIDOR (Python)
┌─────────────────┐            ┌──────────────────────┐
│  Frontend React │  HTTP/JSON │  Backend FastAPI     │
│  (libro cuento) │ ─────────► │  - /predict          │
│                 │ ◄───────── │  - /quiz             │
└─────────────────┘            │  - /quiz/check       │
                               │        │             │
                               │        ▼             │
                               │  Modelo MobileNetV2  │
                               │  (PyTorch)           │
                               └──────────────────────┘
```

- El **frontend** es la interfaz (React + Vite). Se comunica con el backend por
  **peticiones HTTP** que devuelven **JSON**.
- El **backend** (FastAPI) expone una **API REST** con endpoints. Recibe la imagen,
  la preprocesa, se la pasa al modelo y devuelve la predicción.
- El **modelo** (PyTorch) hace la clasificación.
- La **voz** usa la Web Speech API del navegador (no del servidor).

### ¿Por qué separaste frontend y backend?

Separación de responsabilidades: el frontend se encarga de la presentación y el backend
de la lógica e inferencia del modelo. Esto permite que cada parte evolucione por separado
y es una arquitectura estándar (cliente-servidor).

### ¿Qué es una API REST?

Una forma estándar de comunicar dos sistemas por HTTP usando verbos (GET para pedir
datos, POST para enviar datos) y devolviendo datos en formato JSON. Tu `/predict` es un
POST (envías una imagen), tu `/quiz` es un GET (pides una pregunta).

---

## 7. Los diagramas de tu documentación (repásalos)

| Diagrama | Qué muestra | Punto clave |
|----------|-------------|-------------|
| **Clases** | Las clases/servicios del backend y cómo se relacionan | ModelService usa Preprocessor y el AnimalClassifier |
| **Casos de uso** | Qué puede hacer cada actor (Niño, Profesor) | Identificar, jugar quiz, escuchar nombre |
| **Secuencia** | El orden de los mensajes entre componentes | La foto va: frontend → API → preprocess → modelo → respuesta |
| **Máquina de estados** | Los estados por los que pasa el sistema | Portada → Identificar → Quiz → Contraportada |
| **Arquitectura** | Las 3 capas (cliente, servidor, modelo) | Cliente-servidor con API REST |

---

## 8. Validaciones (por si preguntan sobre robustez / calidad del software)

Como es Ingeniería de Software, pueden preguntar cómo manejas errores:

- **En el cliente:** el sistema rechaza archivos que no son imagen (por ejemplo un
  audio) y muy grandes, avisando al usuario.
- **En el servidor:** valida que el archivo sea una imagen válida, que no exceda 10 MB,
  y que los datos del quiz sean correctos. Devuelve códigos de error HTTP (400, 413).
- **Umbral de confianza:** si el modelo no está seguro (menos de 85%), dice "no pude
  reconocer al animal" en vez de dar una respuesta al azar.

---

## 9. Preguntas típicas y cómo responderlas

**¿Por qué elegiste MobileNetV2 y no otra red?**
> Porque es ligera y rápida (diseñada para móviles), entrena rápido y da buena precisión.
> Para 10 clases y un sistema que debe responder rápido, es la opción ideal.

**¿Cómo garantizas que el modelo generaliza y no memoriza?**
> Con data augmentation, dropout, y midiendo sobre un conjunto de validación que el
> modelo nunca vio. Los 94.6% son sobre datos no vistos.

**¿Qué pasa si subo una foto de un animal que no está en las 10 clases?**
> El modelo, al estar forzado a elegir entre 10, daría la más parecida, pero si la
> confianza es menor a 85% el sistema responde "no pude reconocer al animal".

**¿Qué es una imagen para el modelo?**
> Una matriz de números (los píxeles). Una imagen a color de 224×224 es un tensor de
> 224×224×3 (3 canales: rojo, verde, azul).

**¿Qué diferencia hay entre entrenamiento e inferencia?**
> Entrenamiento es cuando el modelo aprende (ajusta sus pesos con los datos). Inferencia
> es cuando ya entrenado, se usa para predecir sobre una imagen nueva. En producción solo
> se hace inferencia.

**¿Por qué usaste PyTorch y no TensorFlow?**
> Porque PyTorch aprovecha la GPU en Windows de forma nativa (TensorFlow ya no lo hace en
> Windows). El entrenamiento en GPU fue de pocos minutos.

**¿Cómo se dice el nombre en voz alta?**
> Con la Web Speech API del navegador (síntesis de voz), configurada en español. No
> requiere internet ni servidor.

**¿Qué mejorarías si tuvieras más tiempo?**
> Más especies, una opción de re-entrenar con fotos nuevas, detección de varios animales
> en una imagen, y persistencia del progreso del niño.

---

## 10. Checklist para el día de la evaluación

- [ ] Llevar la laptop con el proyecto funcionando (probarlo antes de salir de casa).
- [ ] Tener el backend y el frontend listos para arrancar rápido.
- [ ] Tener fotos de animales de prueba a la mano (de las 10 clases).
- [ ] Repasar esta guía, sobre todo **transfer learning** y **las métricas**.
- [ ] Poder explicar cada diagrama de la documentación.
- [ ] Saber dónde está cada cosa en el código por si piden mostrarlo.
- [ ] Tener el `Documentacion.docx` a la mano.

**Consejo final:** no memorices frases; entiende los conceptos para poder explicarlos
con tus palabras y responder repreguntas. Si no sabes algo, es mejor razonar en voz alta
que quedarte callado.
