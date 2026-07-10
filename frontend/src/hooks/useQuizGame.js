// Estado del juego de quiz: prepara N preguntas sin repetir animal

import { useCallback, useEffect, useState } from "react"
import { useSpeech } from "./useSpeech.js"
import { getQuiz, checkQuiz, SPECIES } from "../api/client.js"
import { QUIZ_ROUNDS } from "../config.js"

// Buscar los datos de una especie por su id
function speciesById(id) {
  return SPECIES.find((s) => s.id === id)
}

export function useQuizGame() {
  const [questions, setQuestions] = useState([]) // pregunta por ronda
  const [answers, setAnswers] = useState({}) // { round: { chosen, correct } }
  const { speak } = useSpeech()

  // Cargar preguntas evitando repetir el animal a adivinar
  const load = useCallback(async () => {
    setAnswers({})
    const picked = []
    const usados = new Set()
    while (picked.length < QUIZ_ROUNDS) {
      const q = await getQuiz()
      if (!usados.has(q.imageId)) {
        usados.add(q.imageId)
        picked.push(q)
      }
    }
    setQuestions(picked)
  }, [])

  useEffect(() => {
    load()
  }, [load])

  // Aciertos acumulados y si ya se contesto algo
  const score = Object.values(answers).filter((a) => a.correct).length
  const played = Object.keys(answers).length > 0

  // Responder una pregunta y decir el nombre del animal
  const choose = useCallback(
    async (round, option) => {
      if (answers[round]) return
      const q = questions[round - 1]
      const res = await checkQuiz(q.imageId, option.id)
      setAnswers((prev) => ({ ...prev, [round]: { chosen: option.id, correct: res.correct } }))
      speak(speciesById(res.answerId).name)
    },
    [answers, questions, speak]
  )

  return { questions, answers, score, played, choose, reset: load }
}
