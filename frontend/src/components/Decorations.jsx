// Adornos sueltos (patas y hojas) para vestir las paginas

import AnimalIcon from "./AnimalIcon.jsx"
import "./Decorations.css"

export default function Decorations() {
  return (
    <div className="decorations" aria-hidden="true">
      <span className="deco deco--leaf-1">
        <AnimalIcon src="/leaves-svgrepo-com.svg" size={110} />
      </span>
      <span className="deco deco--paw-1">
        <AnimalIcon src="/paw-svgrepo-com.svg" size={70} />
      </span>
      <span className="deco deco--leaf-2">
        <AnimalIcon src="/leaves-5-svgrepo-com.svg" size={80} />
      </span>
      <span className="deco deco--paw-2">
        <AnimalIcon src="/paw-prints-svgrepo-com.svg" size={85} />
      </span>
    </div>
  )
}
