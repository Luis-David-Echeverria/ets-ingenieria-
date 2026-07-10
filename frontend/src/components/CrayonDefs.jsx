// Filtro SVG que simula el temblor de un trazo hecho a mano, animado

export default function CrayonDefs() {
  return (
    <svg width="0" height="0" aria-hidden="true" style={{ position: "absolute" }}>
      <defs>
        {/* Temblor del trazo: el ruido cambia de semilla para "hervir" (animado) */}
        <filter id="crayon" x="-15%" y="-15%" width="130%" height="130%">
          <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="4" seed="1" result="noise">
            <animate
              attributeName="seed"
              values="1;2;3;4;5"
              dur="0.9s"
              repeatCount="indefinite"
              calcMode="discrete"
            />
          </feTurbulence>
          <feDisplacementMap
            in="SourceGraphic"
            in2="noise"
            scale="3.5"
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
      </defs>
    </svg>
  )
}
