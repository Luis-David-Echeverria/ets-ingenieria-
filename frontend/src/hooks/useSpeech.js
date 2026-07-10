// Hook para hablar en voz alta con la Web Speech API (voz femenina en espanol)

import { useCallback, useEffect, useRef, useState } from "react"
import { SPEECH_LANG } from "../config.js"

// Elegir la mejor voz femenina en espanol disponible
function pickVoice(voices) {
  const spanish = voices.filter((v) => v.lang.toLowerCase().startsWith("es"))
  // Nombres tipicos de voces femeninas por sistema
  const femaleHints = ["female", "mujer", "sabina", "helena", "paulina", "monica", "laura", "google español"]
  const female = spanish.find((v) =>
    femaleHints.some((h) => v.name.toLowerCase().includes(h))
  )
  return female || spanish[0] || null
}

export function useSpeech() {
  const [supported] = useState(() => "speechSynthesis" in window)
  const [speaking, setSpeaking] = useState(false)
  const voiceRef = useRef(null)

  // Cargar las voces (llegan de forma asincrona en algunos navegadores)
  useEffect(() => {
    if (!supported) return
    const load = () => {
      voiceRef.current = pickVoice(window.speechSynthesis.getVoices())
    }
    load()
    window.speechSynthesis.addEventListener("voiceschanged", load)
    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", load)
      window.speechSynthesis.cancel()
    }
  }, [supported])

  // Decir un texto en voz alta, cortando lo anterior
  const speak = useCallback(
    (text) => {
      if (!supported || !text) return
      window.speechSynthesis.cancel()
      const utter = new SpeechSynthesisUtterance(text)
      utter.lang = SPEECH_LANG
      if (voiceRef.current) utter.voice = voiceRef.current
      utter.rate = 0.95
      utter.pitch = 1.15
      utter.onstart = () => setSpeaking(true)
      utter.onend = () => setSpeaking(false)
      utter.onerror = () => setSpeaking(false)
      window.speechSynthesis.speak(utter)
    },
    [supported]
  )

  return { speak, speaking, supported }
}
