"use client"

import { useEffect } from "react"
import { useLocation } from "react-router-dom"

// Este componente detecta cambios en la ruta y desplaza la página hacia arriba
function ScrollToTop() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return null
}

export default ScrollToTop