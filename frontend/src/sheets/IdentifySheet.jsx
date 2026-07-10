// Contenido de identificar: cargar foto, analizar sola, resultado inline hablado

import { useEffect, useState } from "react"
import AnimalIcon from "../components/AnimalIcon.jsx"
import ImageDropzone from "../components/ImageDropzone.jsx"
import { useSpeech } from "../hooks/useSpeech.js"
import { predict } from "../api/client.js"
import { CONFIDENCE_THRESHOLD } from "../config.js"

export function IdentifyRight() {
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const { speak } = useSpeech()

  // Liberar la URL de vista previa al cambiarla
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview)
    }
  }, [preview])

  // Al elegir foto: mostrarla y analizarla automaticamente
  async function handleSelect(picked) {
    setPreview(URL.createObjectURL(picked))
    setResult(null)
    setError(null)
    setLoading(true)
    try {
      const res = await predict(picked)
      setResult(res)
      // Anunciar el nombre solo si la confianza supera el umbral
      if (res.confidence >= CONFIDENCE_THRESHOLD) speak(res.species.name)
    } catch {
      setError("No pude analizar la foto. Intenta de nuevo")
    } finally {
      setLoading(false)
    }
  }

  const recognized = result && result.confidence >= CONFIDENCE_THRESHOLD
  const percent = result ? Math.round(result.confidence * 100) : 0

  return (
    <div className="identify">
      {/* Click en la foto permite cargar otra */}
      <ImageDropzone onSelect={handleSelect} preview={preview} />

      {loading && <p className="face-lead">Pensando...</p>}

      {error && !loading && <p className="identify-unknown">{error}</p>}

      {result && !loading && recognized && (
        <button
          type="button"
          className="identify-answer"
          onClick={() => speak(result.species.name)}
        >
          <AnimalIcon src={result.species.icon} name={result.species.name} size={64} />
          <span className="identify-answer__text">
            <span className="identify-answer__name">{result.species.name}</span>
            <span className="identify-answer__pct">{percent}% de seguridad</span>
          </span>
        </button>
      )}

      {result && !loading && !recognized && (
        <p className="identify-unknown">
          No pude reconocer al animal<br />
          Prueba con otra foto más clara
        </p>
      )}
    </div>
  )
}
