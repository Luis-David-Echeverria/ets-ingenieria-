// Configuracion global del frontend

// URL base del backend. En dev (bun/npm run dev) apunta al backend en :8000.
// En el build servido por el backend queda relativa (mismo origen).
export const BASE_URL = import.meta.env.VITE_API_URL ?? ""

// Usar datos simulados mientras el backend no exista
export const USE_MOCK = false

// Idioma para la sintesis de voz
export const SPEECH_LANG = "es-MX"

// Numero de preguntas por ronda de quiz
export const QUIZ_ROUNDS = 6

// Confianza minima para dar por reconocido un animal
export const CONFIDENCE_THRESHOLD = 0.85
