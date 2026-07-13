# ETS - Clasificador de animales

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```

Abrir: http://localhost:8000 (el backend sirve tambien el build del frontend).

## Frontend

Regenerar el build:

```bash
cd frontend
npm install
npm run build
```

Modo desarrollo (con el backend corriendo aparte):

```bash
cd frontend
npm install
npm run dev
```

## Re-entrenar el modelo

Requiere el dataset en `archive/raw-img/`.

```bash
cd backend
python train.py
```
