// Libro lineal fijo: portada, identificar+invitacion, 5 preguntas de quiz, contraportada

import { useCallback, useRef } from "react"
import HTMLFlipBook from "react-pageflip"
import { QUIZ_ROUNDS } from "../config.js"
import Page from "./Page.jsx"
import BookCover from "./BookCover.jsx"
import Decorations from "./Decorations.jsx"
import { IdentifyRight } from "../sheets/IdentifySheet.jsx"
import { useQuizGame } from "../hooks/useQuizGame.js"
import QuizPage from "../sheets/QuizSheet.jsx"
import CreditsSheet from "../sheets/CreditsSheet.jsx"

export default function Book() {
  const bookRef = useRef(null)
  const lastPage = useRef(0)
  const game = useQuizGame()

  // Al volver a la portada regenerar el quiz con nuevas preguntas
  const handleFlip = useCallback(
    (e) => {
      const page = e.data
      const came = lastPage.current
      lastPage.current = page
      if (page === 0 && came > 0) game.reset()
    },
    [game]
  )

  // Construir las paginas de quiz (una por pregunta), como hijos planos.
  // Identificar e invitacion son las paginas 1 y 2; el quiz sigue desde la 3.
  const quizPages = []
  for (let round = 1; round <= QUIZ_ROUNDS; round++) {
    const question = game.questions[round - 1]
    const answer = game.answers[round]
    quizPages.push(
      <QuizPage
        key={`q-${round}`}
        round={round}
        question={question}
        answer={answer}
        onChoose={game.choose}
        pageNumber={2 + round}
      />
    )
  }

  return (
    <div className="book-stage">
      <HTMLFlipBook
        ref={bookRef}
        className="flip-book"
        width={460}
        height={630}
        size="fixed"
        showCover={true}
        drawShadow={true}
        maxShadowOpacity={0.6}
        flippingTime={800}
        showPageCorners={false}
        useMouseEvents={true}
        clickEventForward={false}
        disableFlipByClick={true}
        mobileScrollSupport={true}
        onFlip={handleFlip}
      >
        {/* Portada */}
        <BookCover variant="front" image="/Portada.png" />

        {/* Spread Identificar (izq) + invitacion al quiz (der) */}
        <Page side="left" title="Identificar" number={1}>
          <IdentifyRight />
        </Page>
        <Page side="right" number={2}>
          <Decorations />
          <div className="invite">
            <h2 className="invite__title">¡A jugar!</h2>
            <p className="invite__text">
              Pasa la página y adivina quién se esconde. ¿Podrás reconocer a todos
              los animales del cuento?
            </p>
          </div>
        </Page>

        {/* Quiz: una pregunta por spread */}
        {quizPages}

        {/* Contraportada con estrellas y creditos */}
        <BookCover variant="back">
          <CreditsSheet score={game.score} played={game.played} />
        </BookCover>
      </HTMLFlipBook>
    </div>
  )
}
