// Quiz: cada pregunta en UNA sola pagina (icono + opciones de nombre)

import { forwardRef } from "react"
import Page from "../components/Page.jsx"
import AnimalIcon from "../components/AnimalIcon.jsx"
import { SPECIES } from "../api/client.js"

// Buscar los datos de una especie por su id
function speciesById(id) {
  return SPECIES.find((s) => s.id === id)
}

// Una pregunta completa en una sola pagina
const QuizPage = forwardRef(function QuizPage(
  { round, question, answer, onChoose, pageNumber },
  ref
) {
  const animal = question ? speciesById(question.imageId) : null
  const answered = Boolean(answer)

  return (
    <Page ref={ref} side="right" number={pageNumber}>
      {!question ? (
        <p className="face-lead">Preparando...</p>
      ) : (
        <div className="quiz">
          {/* Animal a adivinar */}
          <AnimalIcon src={animal.icon} name={animal.name} size={130} />
          <p className="quiz__hint">
            {answered
              ? answer.correct
                ? "¡Correcto!"
                : `Es ${animal.article} ${animal.name}`
              : "¿Cómo se llama este animal?"}
          </p>

          {/* Opciones de nombre */}
          <div className="quiz-names">
            {question.options.map((option) => {
              let state = "idle"
              if (answered) {
                if (option.id === question.answerId) state = "correct"
                else if (option.id === answer.chosen) state = "wrong"
              }
              return (
                <button
                  key={option.id}
                  type="button"
                  className={`name-btn name-btn--${state}`}
                  disabled={answered}
                  onClick={() => onChoose(round, option)}
                >
                  {option.name}
                </button>
              )
            })}
          </div>
        </div>
      )}
    </Page>
  )
})

export default QuizPage
