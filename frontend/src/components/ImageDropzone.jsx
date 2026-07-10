// Zona para subir y previsualizar una imagen

import { useRef, useState } from "react"
import { motion } from "motion/react"
import AnimalIcon from "./AnimalIcon.jsx"
import "./ImageDropzone.css"

// Tamano maximo aceptado en el cliente (10 MB)
const MAX_BYTES = 10 * 1024 * 1024

export default function ImageDropzone({ onSelect, preview }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState(null)

  // Validar el archivo elegido antes de entregarlo
  function handleFile(file) {
    if (!file) return
    if (!file.type.startsWith("image/")) {
      setError("Eso no es una foto, elige una imagen")
      return
    }
    if (file.size > MAX_BYTES) {
      setError("La foto es muy grande (máximo 10 MB)")
      return
    }
    setError(null)
    onSelect(file)
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  return (
    <motion.div
      className={`dropzone ${dragging ? "dropzone--active" : ""}`}
      onClick={() => inputRef.current.click()}
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      whileHover={{ scale: 1.01 }}
    >
      {preview ? (
        <img className="dropzone__preview" src={preview} alt="Imagen elegida" />
      ) : (
        <div className="dropzone__hint">
          <AnimalIcon src="/camera-svgrepo-com.svg" name="Cámara" size={70} />
          <p>Toca aquí para elegir una foto</p>
          <small className={error ? "dropzone__error" : ""}>
            {error || "o arrástrala hasta el libro"}
          </small>
        </div>
      )}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="sr-only"
        onChange={(e) => handleFile(e.target.files[0])}
      />
    </motion.div>
  )
}
