// Cliente HTTP hacia el backend FastAPI (con modo simulado)

import { BASE_URL, USE_MOCK } from "../config.js"

// Catalogo base de especies (Animals-10) con icono SVG y articulo por genero
export const SPECIES = [
  { id: "perro", name: "Perro", icon: "/dog-svgrepo-com.svg", article: "un" },
  { id: "gato", name: "Gato", icon: "/cat-svgrepo-com.svg", article: "un" },
  { id: "caballo", name: "Caballo", icon: "/alpaca-svgrepo-com.svg", article: "un" },
  { id: "elefante", name: "Elefante", icon: "/elephant-svgrepo-com.svg", article: "un" },
  { id: "mariposa", name: "Mariposa", icon: "/butterfly-svgrepo-com.svg", article: "una" },
  { id: "gallina", name: "Gallina", icon: "/rooster-svgrepo-com.svg", article: "una" },
  { id: "vaca", name: "Vaca", icon: "/the-cow-svgrepo-com.svg", article: "una" },
  { id: "oveja", name: "Oveja", icon: "/mianyang-svgrepo-com.svg", article: "una" },
  { id: "arana", name: "Araña", icon: "/spider-svgrepo-com.svg", article: "una" },
  { id: "ardilla", name: "Ardilla", icon: "/squirrel-svgrepo-com.svg", article: "una" },
]

// Elegir un elemento aleatorio de una lista
function pickRandom(list) {
  return list[Math.floor(Math.random() * list.length)]
}

// Simular una espera de red
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Obtener la lista de especies reconocidas
export async function getSpecies() {
  if (USE_MOCK) {
    await delay(200)
    return SPECIES
  }
  const res = await fetch(`${BASE_URL}/species`)
  return res.json()
}

// Enviar una imagen y recibir la especie predicha
export async function predict(file) {
  if (USE_MOCK) {
    await delay(900)
    const guess = pickRandom(SPECIES)
    return { species: guess, confidence: 0.7 + Math.random() * 0.29 }
  }
  const form = new FormData()
  form.append("file", file)
  const res = await fetch(`${BASE_URL}/predict`, { method: "POST", body: form })
  return res.json()
}

// Obtener una pregunta de quiz (imagen + opciones)
export async function getQuiz() {
  if (USE_MOCK) {
    await delay(400)
    const answer = pickRandom(SPECIES)
    // Armar dos distractores distintos a la respuesta
    const others = SPECIES.filter((s) => s.id !== answer.id)
    const distractors = [...others].sort(() => Math.random() - 0.5).slice(0, 2)
    const options = [answer, ...distractors].sort(() => Math.random() - 0.5)
    return { imageId: answer.id, answerId: answer.id, options }
  }
  const res = await fetch(`${BASE_URL}/quiz`)
  return res.json()
}

// Validar la respuesta elegida en el quiz
export async function checkQuiz(imageId, choiceId) {
  if (USE_MOCK) {
    await delay(150)
    return { correct: imageId === choiceId, answerId: imageId }
  }
  const res = await fetch(`${BASE_URL}/quiz/check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ imageId, choiceId }),
  })
  return res.json()
}
