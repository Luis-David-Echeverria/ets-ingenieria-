// Tapa dura del libro (portada o contraportada), con forwardRef

import { forwardRef } from "react"

const BookCover = forwardRef(function BookCover({ variant = "front", image, children }, ref) {
  // Portada como imagen a sangre completa, sin overlay
  if (image) {
    return (
      <div className={`page ${variant === "back" ? "page--left" : "page--right"}`} ref={ref} data-density="hard">
        <div className="cover cover--image" style={{ backgroundImage: `url(${image})` }} />
      </div>
    )
  }

  return (
    <div className={`page ${variant === "back" ? "page--left" : "page--right"}`} ref={ref} data-density="hard">
      <div className={`cover ${variant === "back" ? "cover--back" : ""}`}>{children}</div>
    </div>
  )
})

export default BookCover
