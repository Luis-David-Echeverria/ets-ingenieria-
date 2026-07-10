// Fila de estrellas de puntuacion (llenas segun aciertos)

import "./Stars.css"

export default function Stars({ score, total }) {
  return (
    <div className="stars" aria-label={`${score} de ${total} estrellas`}>
      {Array.from({ length: total }, (_, i) => (
        <img
          key={i}
          className="stars__item"
          src={i < score ? "/star-svgrepo-com filled.svg" : "/star-svgrepo-com (1).svg"}
          alt=""
        />
      ))}
    </div>
  )
}
