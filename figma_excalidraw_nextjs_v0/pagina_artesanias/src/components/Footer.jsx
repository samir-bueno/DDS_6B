"use client"

import { useState } from "react"
import { Link } from "react-router-dom"
import "../hojas-de-estilo/Footer.css"
import Toast from "./Toast"

function Footer() {
  // Estado para el formulario
  const [formData, setFormData] = useState({
    nombre: "",
    email: "",
    asunto: "",
    mensaje: "",
  })

  // Estado para errores de validación
  const [errors, setErrors] = useState({})

  // Estado para el toast
  const [toast, setToast] = useState({
    show: false,
    message: "",
    type: "success",
  })

  // Manejar cambios en los campos del formulario
  const handleChange = (e) => {
    const { id, value } = e.target
    setFormData({
      ...formData,
      [id]: value,
    })

    // Limpiar error cuando el usuario escribe
    if (errors[id]) {
      setErrors({
        ...errors,
        [id]: "",
      })
    }
  }

  // Validar email con expresión regular
  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  // Validar el formulario
  const validateForm = () => {
    const newErrors = {}

    // Validar campos requeridos
    if (!formData.nombre.trim()) {
      newErrors.nombre = "El nombre es requerido"
    }

    if (!formData.email.trim()) {
      newErrors.email = "El correo electrónico es requerido"
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = "Ingresa un correo electrónico válido"
    }

    if (!formData.asunto.trim()) {
      newErrors.asunto = "El asunto es requerido"
    }

    if (!formData.mensaje.trim()) {
      newErrors.mensaje = "El mensaje es requerido"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Manejar envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault()

    // Validar formulario
    if (validateForm()) {
      // Mostrar el objeto formData en la consola
      console.log({
        nombre: formData.nombre,
        email: formData.email,
        asunto: formData.asunto,
        mensaje: formData.mensaje,
      })

      // Mostrar mensaje de éxito
      setToast({
        show: true,
        message: "¡Mensaje enviado con éxito!",
        type: "success",
      })

      // Limpiar formulario
      setFormData({
        nombre: "",
        email: "",
        asunto: "",
        mensaje: "",
      })
    }
  }

  // Cerrar el toast
  const closeToast = () => {
    setToast({ ...toast, show: false })
  }

  return (
    <footer id="contacto" className="footer">
      <div className="container">
        <div className="footer-grid">
          <div className="contact-section">
            {/* Título "Contáctanos" con estilo inline para mayor visibilidad */}
            <h2
              style={{
                fontSize: "2.25rem",
                fontFamily: "var(--font-serif)",
                fontWeight: "700",
                color: "#FFFFFF",
                marginBottom: "1rem",
                textShadow: "0 1px 3px rgba(0,0,0,0.3)",
              }}
            >
              Contáctanos
            </h2>
            {/* Texto descriptivo con estilo inline */}
            <p
              style={{
                color: "#FFFFFF",
                fontWeight: "600",
                marginBottom: "1.5rem",
                fontSize: "1.125rem",
                textShadow: "0 1px 2px rgba(0,0,0,0.3)",
              }}
            >
              Completa el formulario y nos pondremos en contacto contigo lo antes posible.
            </p>

            <div className="contact-form-container">
              <form className="contact-form" onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="nombre" className="form-label">
                    Nombre
                  </label>
                  <input
                    id="nombre"
                    placeholder="Tu nombre"
                    className={`form-input ${errors.nombre ? "input-error" : ""}`}
                    value={formData.nombre}
                    onChange={handleChange}
                  />
                  {errors.nombre && <p className="error-message">{errors.nombre}</p>}
                </div>

                <div className="form-group">
                  <label htmlFor="email" className="form-label">
                    Correo Electrónico
                  </label>
                  <input
                    id="email"
                    type="email"
                    placeholder="tucorreo@ejemplo.com"
                    className={`form-input ${errors.email ? "input-error" : ""}`}
                    value={formData.email}
                    onChange={handleChange}
                  />
                  {errors.email && <p className="error-message">{errors.email}</p>}
                </div>

                <div className="form-group">
                  <label htmlFor="asunto" className="form-label">
                    Asunto
                  </label>
                  <input
                    id="asunto"
                    placeholder="¿En qué podemos ayudarte?"
                    className={`form-input ${errors.asunto ? "input-error" : ""}`}
                    value={formData.asunto}
                    onChange={handleChange}
                  />
                  {errors.asunto && <p className="error-message">{errors.asunto}</p>}
                </div>

                <div className="form-group">
                  <label htmlFor="mensaje" className="form-label">
                    Mensaje
                  </label>
                  <textarea
                    id="mensaje"
                    placeholder="Escribe tu mensaje aquí..."
                    rows={4}
                    className={`form-textarea ${errors.mensaje ? "input-error" : ""}`}
                    value={formData.mensaje}
                    onChange={handleChange}
                  />
                  {errors.mensaje && <p className="error-message">{errors.mensaje}</p>}
                </div>

                <button type="submit" className="submit-button">
                  Enviar Mensaje
                </button>
              </form>
            </div>
          </div>

          <div className="footer-info">
            {/* Primera fila: Enlaces Rápidos y Categorías */}
            <div className="footer-top-row">
              {/* Enlaces Rápidos */}
              <div className="links-section">
                <h3 className="footer-heading">Enlaces Rápidos</h3>
                <ul className="footer-links">
                  <li>
                    <Link to="/" className="footer-link">
                      Inicio
                    </Link>
                  </li>
                  <li>
                    <Link to="/productos" className="footer-link">
                      Productos
                    </Link>
                  </li>
                  <li>
                    <Link to="/sobre-nosotros" className="footer-link">
                      Sobre Nosotros
                    </Link>
                  </li>
                  <li>
                    <a href="#contacto" className="footer-link">
                      Contacto
                    </a>
                  </li>
                </ul>
              </div>

              {/* Categorías */}
              <div className="categories-section">
                <h3 className="footer-heading">Categorías</h3>
                <ul className="footer-links">
                  <li>
                    <Link to="/productos?categoria=cerámica" className="footer-link">
                      Cerámica
                    </Link>
                  </li>
                  <li>
                    <Link to="/productos?categoria=textiles" className="footer-link">
                      Textiles
                    </Link>
                  </li>
                  <li>
                    <Link to="/productos?categoria=joyería" className="footer-link">
                      Joyería
                    </Link>
                  </li>
                </ul>
              </div>
            </div>

            {/* Segunda fila: Redes Sociales y Contacto */}
            <div className="footer-bottom-row">
              {/* Redes Sociales */}
              <div className="social-section">
                <h3 className="footer-heading">Redes Sociales</h3>
                <ul className="footer-links">
                  <li>
                    <a
                      href="https://www.facebook.com"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="footer-link"
                    >
                      Facebook
                    </a>
                  </li>
                  <li>
                    <a
                      href="https://www.instagram.com"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="footer-link"
                    >
                      Instagram
                    </a>
                  </li>
                </ul>
              </div>

              {/* Contacto */}
              <div className="contact-info-section">
                <h3 className="footer-heading">Contacto</h3>
                <ul className="contact-info">
                  <li className="contact-item">
                    <a href="mailto:info@manoscreativas.com" className="contact-text">
                      info@manoscreativas.com
                    </a>
                  </li>
                  <li className="contact-item">
                    <a href="tel:+521234567890" className="contact-text">
                      +52 (123) 456-7890
                    </a>
                  </li>
                  <li className="contact-item">
                    <a
                      href="https://maps.google.com/?q=Calle+Artesanos+123+Colonia+Centro+Ciudad+Artesanal"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="contact-text"
                    >
                      Calle Artesanos #123
                      <br />
                      Colonia Centro
                      <br />
                      Ciudad Artesanal, CP 12345
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Toast de notificación */}
      {toast.show && <Toast message={toast.message} type={toast.type} onClose={closeToast} />}
    </footer>
  )
}

export default Footer