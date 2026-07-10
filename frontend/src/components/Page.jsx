// Pagina del flipbook (requiere forwardRef para StPageFlip)

import { forwardRef } from "react"

// side controla el pliegue hacia el lomo; density "hard" para tapas
const Page = forwardRef(function Page(
  { title, number, side = "right", hard = false, children },
  ref
) {
  return (
    <div className={`page page--${side}`} ref={ref} data-density={hard ? "hard" : "soft"}>
      <div className="face">
        {title && (
          <header className="face-head">
            <h2 className="face-title">{title}</h2>
          </header>
        )}
        <div className="face-body">{children}</div>
        {number && <span className="face-number">— {number} —</span>}
      </div>
    </div>
  )
})

export default Page
