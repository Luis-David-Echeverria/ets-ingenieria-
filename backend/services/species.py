"""Catalogo de especies del dataset Animals-10 (en espanol)."""

# Mapear el nombre de carpeta (italiano) del dataset al id/etiqueta en espanol
FOLDER_TO_ID = {
    "cane": "perro",
    "gatto": "gato",
    "cavallo": "caballo",
    "elefante": "elefante",
    "farfalla": "mariposa",
    "gallina": "gallina",
    "mucca": "vaca",
    "pecora": "oveja",
    "ragno": "arana",
    "scoiattolo": "ardilla",
}

# Datos de cada especie que consume el frontend
SPECIES = [
    {"id": "perro", "name": "Perro", "icon": "/dog-svgrepo-com.svg", "article": "un"},
    {"id": "gato", "name": "Gato", "icon": "/cat-svgrepo-com.svg", "article": "un"},
    {"id": "caballo", "name": "Caballo", "icon": "/alpaca-svgrepo-com.svg", "article": "un"},
    {"id": "elefante", "name": "Elefante", "icon": "/elephant-svgrepo-com.svg", "article": "un"},
    {"id": "mariposa", "name": "Mariposa", "icon": "/butterfly-svgrepo-com.svg", "article": "una"},
    {"id": "gallina", "name": "Gallina", "icon": "/rooster-svgrepo-com.svg", "article": "una"},
    {"id": "vaca", "name": "Vaca", "icon": "/the-cow-svgrepo-com.svg", "article": "una"},
    {"id": "oveja", "name": "Oveja", "icon": "/mianyang-svgrepo-com.svg", "article": "una"},
    {"id": "arana", "name": "Araña", "icon": "/spider-svgrepo-com.svg", "article": "una"},
    {"id": "ardilla", "name": "Ardilla", "icon": "/squirrel-svgrepo-com.svg", "article": "una"},
]

# Indice rapido por id
BY_ID = {s["id"]: s for s in SPECIES}


def get_species(species_id):
    """Devolver los datos de una especie por su id."""
    return BY_ID.get(species_id)
