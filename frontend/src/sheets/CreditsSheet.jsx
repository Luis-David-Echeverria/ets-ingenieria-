// Contenido de la contraportada (dentro de BookCover variant="back")

import Stars from "../components/Stars.jsx"
import { QUIZ_ROUNDS } from "../config.js"

export default function CreditsSheet({ score, played }) {
  return (
    <>
      <h1 className="cover__title">Fin del cuento</h1>

      {played && (
        <div className="credits-score">
          <Stars score={score} total={QUIZ_ROUNDS} />
          <p>Acertaste {score} de {QUIZ_ROUNDS} animales</p>
        </div>
      )}

      <p className="credits-hint">
        Vuelve a la portada para leer el cuento otra vez
      </p>

      <dl className="credits-list">
        <div className="credits-row">
          <dt>Alumno</dt>
          <dd>Luis David Echeverría Pérez</dd>
        </div>
        <div className="credits-row">
          <dt>Boleta</dt>
          <dd>2022630724</dd>
        </div>
        <div className="credits-row">
          <dt>Carrera</dt>
          <dd>Ing. en IA</dd>
        </div>
        <div className="credits-row">
          <dt>Profesora</dt>
          <dd>Idalia Maldonado Castillo</dd>
        </div>
      </dl>
    </>
  )
}
