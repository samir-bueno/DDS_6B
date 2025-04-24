"use client"

import { useState, useEffect } from "react"
import { Link, useLocation } from "react-router-dom"
import logo from '../imagenes/logo_artesanal.png'
import "../hojas-de-estilo/Header.css"

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()

  // Efecto para prevenir el scroll cuando el menú está abierto
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = "auto"
    }

    return () => {
      document.body.style.overflow = "auto"
    }
  }, [isMenuOpen])

  // Función para manejar el clic en el enlace de contacto
  const handleContactClick = (e) => {
    e.preventDefault()
    setIsMenuOpen(false)

    const contactElement = document.getElementById("contacto")
    if (contactElement) {
      contactElement.scrollIntoView({ behavior: "smooth" })
    }
  }

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  const closeMenu = () => {
    setIsMenuOpen(false)
  }

  // Función para desplazar al inicio de la página cuando se navega a una nueva ruta
  const scrollToTop = () => {
    window.scrollTo(0, 0)
  }

  const links = [
    { href: "/", label: "Inicio" },
    { href: "/productos", label: "Productos" },
    { href: "/sobre-nosotros", label: "Sobre Nosotros" },
    { href: "#contacto", label: "Contacto", onClick: handleContactClick },
  ]

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo-container">
            <Link to="/" className="logo-link" onClick={scrollToTop}>
              <div className="logo">
                <img src={logo} alt="Manos Creativas Logo" />
              </div>
              <span className="logo-text">Manos Creativas</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="desktop-nav">
            {links.map((link) => (
              <Link
                key={link.href}
                to={link.href.startsWith("#") ? link.href : link.href}
                className="nav-link"
                onClick={link.onClick || (link.href.startsWith("#") ? null : scrollToTop)}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <div className="mobile-menu">
            <button className="menu-button" onClick={toggleMenu} aria-label="Abrir menú">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Menú móvil */}
      {isMenuOpen && (
        <div className="menu-overlay">
          <div className="menu-content">
            <button className="close-button" onClick={closeMenu} aria-label="Cerrar menú">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>

            <h2 className="mobile-menu-title">Menú</h2>

            <nav className="mobile-nav">
              {links.map((link) => (
                <Link
                  key={link.href}
                  to={link.href.startsWith("#") ? link.href : link.href}
                  className="nav-link"
                  onClick={(e) => {
                    if (link.onClick) {
                      link.onClick(e)
                    } else if (!link.href.startsWith("#")) {
                      closeMenu()
                      scrollToTop()
                    } else {
                      closeMenu()
                    }
                  }}
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      )}
    </header>
  )
}

export default Header