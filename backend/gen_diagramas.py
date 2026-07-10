"""Genera los diagramas de la documentacion como PNG (Graphviz + matplotlib).

Uso: python gen_diagramas.py
Guarda los PNG en ../docs/imagenes/.
"""

from pathlib import Path

from graphviz import Digraph

OUT = Path(__file__).resolve().parent.parent / "docs" / "imagenes"
OUT.mkdir(parents=True, exist_ok=True)

# Estilo comun de los diagramas
BASE_ATTRS = {"fontname": "Segoe UI", "bgcolor": "white"}
NODE_ATTRS = {"fontname": "Segoe UI", "style": "filled", "fillcolor": "#fef6e4"}


def guardar(dot, nombre):
    """Renderizar un diagrama a PNG."""
    dot.render(OUT / nombre, format="png", cleanup=True)
    print("Generado", nombre + ".png")


def diagrama_clases():
    dot = Digraph("clases", graph_attr={**BASE_ATTRS, "rankdir": "TB"})
    dot.attr("node", shape="record", **NODE_ATTRS)

    dot.node("API", "{API|+ list_species()\\l+ predict(file)\\l+ get_quiz()\\l+ check_quiz()\\l+ health()\\l}")
    dot.node("Model", "{ModelService|- model\\l- labels\\l+ is_ready()\\l+ predict(bytes)\\l}")
    dot.node("Pre", "{Preprocessor|+ IMG_SIZE\\l+ prepare_image(bytes)\\l}")
    dot.node("Quiz", "{QuizService|+ make_question()\\l+ check_answer()\\l}")
    dot.node("Clf", "{AnimalClassifier\\n(MobileNetV2)|+ features (congelado)\\l+ classifier (10 clases)\\l+ forward(tensor)\\l}")
    dot.node("Species", "{Species|+ id\\l+ name\\l+ icon\\l+ article\\l}")
    dot.node("Pred", "{Prediction|+ species\\l+ confidence\\l}")
    dot.node("Question", "{Question|+ imageId\\l+ answerId\\l+ options\\l}")
    dot.node("Result", "{Result|+ correct\\l+ answerId\\l}")

    dot.edge("API", "Model", "usa", style="dashed")
    dot.edge("API", "Quiz", "usa", style="dashed")
    dot.edge("Model", "Pre", "usa", style="dashed")
    dot.edge("Model", "Clf", "infiere", style="dashed")
    dot.edge("Model", "Pred", "produce")
    dot.edge("Quiz", "Question", "produce")
    dot.edge("Quiz", "Result", "produce")
    dot.edge("Question", "Species", "contiene", arrowhead="diamond", dir="back")
    dot.edge("Pred", "Species", "contiene", arrowhead="diamond", dir="back")
    guardar(dot, "clases")


def diagrama_casos_uso():
    dot = Digraph("casos", graph_attr={**BASE_ATTRS, "rankdir": "LR"})
    dot.attr("node", **NODE_ATTRS)

    # Actores
    dot.node("Nino", "Niño", shape="box", fillcolor="#cdeef5")
    dot.node("Prof", "Profesor", shape="box", fillcolor="#cdeef5")

    casos = {
        "UC1": "Abrir el libro",
        "UC2": "Identificar animal\npor foto",
        "UC3": "Escuchar el nombre\nen voz alta",
        "UC4": "Jugar al quiz",
        "UC5": "Responder pregunta\nopción múltiple",
        "UC6": "Ver resultado\ny estrellas",
        "UC7": "Ver créditos\ndel autor",
    }
    for k, v in casos.items():
        dot.node(k, v, shape="ellipse")

    for uc in ["UC1", "UC2", "UC4", "UC5", "UC6"]:
        dot.edge("Nino", uc)
    for uc in ["UC2", "UC4", "UC7"]:
        dot.edge("Prof", uc)

    dot.edge("UC2", "UC3", "«include»", style="dashed")
    dot.edge("UC5", "UC3", "«include»", style="dashed")
    dot.edge("UC4", "UC5", "«include»", style="dashed")
    dot.edge("UC5", "UC6", "«extend»", style="dashed")
    guardar(dot, "casos-de-uso")


def diagrama_arquitectura():
    dot = Digraph("arq", graph_attr={**BASE_ATTRS, "rankdir": "TB"})
    dot.attr("node", **NODE_ATTRS)

    with dot.subgraph(name="cluster_cli") as c:
        c.attr(label="Cliente", style="filled", fillcolor="#f0f7ff", fontname="Segoe UI")
        c.node("FE", "Frontend\nReact + Vite\n(Libro interactivo)", shape="box")
    with dot.subgraph(name="cluster_srv") as c:
        c.attr(label="Servidor", style="filled", fillcolor="#fff3e4", fontname="Segoe UI")
        c.node("BE", "Backend FastAPI\n(REST API)", shape="box")
        c.node("SVC", "Servicios\nPreprocess · Model · Quiz", shape="box")
        c.node("MODEL", "MobileNetV2\nentrenado", shape="cylinder", fillcolor="#eaf8e0")

    dot.node("DS", "Dataset\nAnimals-10", shape="cylinder", fillcolor="#fdecee")
    dot.edge("FE", "BE", "HTTP / JSON")
    dot.edge("BE", "SVC")
    dot.edge("SVC", "MODEL")
    dot.edge("DS", "MODEL", "entrenamiento offline", style="dashed")
    guardar(dot, "arquitectura")


def diagrama_secuencia_identificar():
    # Secuencia simplificada como grafo de flujo (graphviz no hace UML sequence nativo)
    dot = Digraph("seq_id", graph_attr={**BASE_ATTRS, "rankdir": "TB"})
    dot.attr("node", shape="box", **NODE_ATTRS)
    pasos = [
        ("s1", "Niño sube una foto"),
        ("s2", "Frontend: vista previa\nPOST /predict"),
        ("s3", "Backend: prepare_image()\nresize 224x224 + normaliza"),
        ("s4", "AnimalClassifier.forward()\n→ probabilidades"),
        ("s5", "Backend: argmax + softmax\n→ {species, confidence}"),
        ("s6", "¿confianza ≥ 85%?"),
        ("s7", "Muestra ícono + nombre + %\ny dice el nombre (voz)"),
        ("s8", "\"No pude reconocer\nal animal\""),
    ]
    for k, v in pasos:
        shape = "diamond" if k == "s6" else "box"
        dot.node(k, v, shape=shape)
    for a, b in [("s1", "s2"), ("s2", "s3"), ("s3", "s4"), ("s4", "s5"), ("s5", "s6")]:
        dot.edge(a, b)
    dot.edge("s6", "s7", "sí")
    dot.edge("s6", "s8", "no")
    guardar(dot, "secuencia-identificar")


def diagrama_secuencia_quiz():
    dot = Digraph("seq_quiz", graph_attr={**BASE_ATTRS, "rankdir": "TB"})
    dot.attr("node", shape="box", **NODE_ATTRS)
    pasos = [
        ("q1", "GET /quiz"),
        ("q2", "QuizService.make_question()\nanimal + 2 distractores"),
        ("q3", "Muestra ícono + 3 nombres"),
        ("q4", "Niño elige un nombre"),
        ("q5", "POST /quiz/check"),
        ("q6", "check_answer()\n→ {correct, answerId}"),
        ("q7", "Marca verde/rojo + estrella\ny dice el nombre"),
    ]
    for k, v in pasos:
        dot.node(k, v)
    for a, b in zip([p[0] for p in pasos], [p[0] for p in pasos[1:]]):
        dot.edge(a, b)
    guardar(dot, "secuencia-quiz")


def maquina_estados_libro():
    dot = Digraph("est_libro", graph_attr={**BASE_ATTRS, "rankdir": "LR"})
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="#fef6e4", fontname="Segoe UI")
    dot.node("ini", "", shape="circle", width="0.2", fillcolor="black")
    dot.node("Portada", "Portada")
    dot.node("Identificar", "Identificar")
    dot.node("Invitacion", "Invitación")
    dot.node("Quiz", "Quiz")
    dot.node("Contra", "Contraportada")
    dot.edge("ini", "Portada")
    dot.edge("Portada", "Identificar", "pasar página")
    dot.edge("Identificar", "Invitacion", "página derecha")
    dot.edge("Invitacion", "Quiz", "pasar página")
    dot.edge("Quiz", "Quiz", "siguiente pregunta")
    dot.edge("Quiz", "Contra", "tras 6 preguntas")
    dot.edge("Contra", "Portada", "volver (reinicia)")
    guardar(dot, "maquina-estados-libro")


def maquina_estados_quiz():
    dot = Digraph("est_quiz", graph_attr={**BASE_ATTRS, "rankdir": "LR"})
    dot.attr("node", shape="box", style="rounded,filled", fillcolor="#fef6e4", fontname="Segoe UI")
    dot.node("ini", "", shape="circle", width="0.2", fillcolor="black")
    dot.node("Sin", "Sin responder")
    dot.node("OK", "Correcta", fillcolor="#eaf8e0")
    dot.node("NO", "Incorrecta", fillcolor="#fdecee")
    dot.node("fin", "", shape="doublecircle", width="0.2", fillcolor="black")
    dot.edge("ini", "Sin")
    dot.edge("Sin", "OK", "opción correcta")
    dot.edge("Sin", "NO", "opción incorrecta")
    dot.edge("OK", "fin", "nombre + estrella")
    dot.edge("NO", "fin", "dice el correcto")
    guardar(dot, "maquina-estados-quiz")


if __name__ == "__main__":
    diagrama_clases()
    diagrama_casos_uso()
    diagrama_arquitectura()
    diagrama_secuencia_identificar()
    diagrama_secuencia_quiz()
    maquina_estados_libro()
    maquina_estados_quiz()
    print("Listo. Diagramas en", OUT)
