# Diagrama de Clases

Representa las clases y servicios principales del sistema, tanto del backend
(Python/FastAPI) como de los servicios del modelo de IA.

```mermaid
classDiagram
    class API {
        +list_species() list~Species~
        +predict(file) Prediction
        +get_quiz() Question
        +check_quiz(imageId, choiceId) Result
        +health() Status
    }

    class Species {
        +str id
        +str name
        +str icon
        +str article
    }

    class ModelService {
        -model
        -labels
        -device
        +is_ready() bool
        +predict(bytes) Prediction
        -_load()
    }

    class Preprocessor {
        +IMG_SIZE int
        +prepare_image(bytes) Tensor
    }

    class QuizService {
        +make_question() Question
        +check_answer(imageId, choiceId) Result
    }

    class Prediction {
        +Species species
        +float confidence
    }

    class Question {
        +str imageId
        +str answerId
        +Species[] options
    }

    class Result {
        +bool correct
        +str answerId
    }

    class AnimalClassifier {
        <<MobileNetV2>>
        +features (congelado)
        +classifier (10 clases)
        +forward(tensor) logits
    }

    API ..> ModelService : usa
    API ..> QuizService : usa
    API ..> Species : devuelve
    ModelService ..> Preprocessor : usa
    ModelService ..> AnimalClassifier : carga e infiere
    ModelService --> Prediction : produce
    QuizService --> Question : produce
    QuizService --> Result : produce
    Question o-- Species : contiene opciones
    Prediction o-- Species : contiene
```

## Descripción de clases

| Clase | Responsabilidad |
|-------|-----------------|
| **API** | Punto de entrada FastAPI. Expone los endpoints REST y orquesta los servicios. |
| **ModelService** | Carga el modelo entrenado (perezoso) y ejecuta la inferencia sobre una imagen. |
| **Preprocessor** | Redimensiona (224×224) y normaliza la imagen antes de la inferencia. |
| **QuizService** | Genera preguntas aleatorias y valida las respuestas del quiz. |
| **AnimalClassifier** | Red neuronal MobileNetV2 con transfer learning (base congelada + cabeza de 10 clases). |
| **Species / Prediction / Question / Result** | Estructuras de datos que viajan entre backend y frontend (DTOs). |
