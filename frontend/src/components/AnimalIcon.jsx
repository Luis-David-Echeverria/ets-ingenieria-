// Icono de animal con textura de crayon (usa <img> para no cruzarse al clonar DOM)

import "./AnimalIcon.css"

export default function AnimalIcon({ src, name, size = 120, crayon = true }) {
  if (!src) return null

  return (
    <img
      className={`animal-icon ${crayon ? "animal-icon--crayon" : ""}`}
      src={src}
      width={size}
      height={size}
      alt={name || ""}
      draggable="false"
    />
  )
}
