import PageHeader from "../components/PageHeader"
import "../hojas-de-estilo/AboutUs.css"
import logo from '../imagenes/logo_artesanal.png'

function AboutUs() {
  const proceso = [
    {
      title: "Selección de materiales",
      description: "Elegimos cuidadosamente materias primas de la más alta calidad y de origen local",
    },
    {
      title: "Diseño tradicional",
      description: "Creamos diseños basados en patrones ancestrales con toques contemporáneos",
    },
    {
      title: "Elaboración artesanal",
      description: "Cada pieza es elaborada a mano por artesanos expertos, sin producción en masa",
    },
    {
      title: "Control de calidad",
      description: "Verificamos que cada artesanía cumpla con nuestros estándares de excelencia",
    },
  ]

  return (
    <div className="about-page">
      <PageHeader
        title="Sobre Nosotros"
        description="Conoce nuestra historia y el proceso artesanal"
        image="https://images.unsplash.com/photo-1605721911519-3dfeb3be25e7"
      />

      {/* Historia */}
      <section className="history-section">
        <div className="container">
          <div className="history-content">
            <div className="history-text">
              <h2 className="section-title">Nuestra Historia</h2>
              <div className="history-paragraphs">
                <p>
                  Manos Creativas nació en 1985 como un pequeño taller familiar en el corazón de un pueblo artesanal. Lo
                  que comenzó como un sueño de preservar las técnicas tradicionales, se ha convertido en un referente de
                  la artesanía auténtica en la región.
                </p>
                <p>
                  Fundada por Don Miguel Hernández, maestro artesano con más de 40 años de experiencia, nuestra tienda
                  ha crecido gracias al compromiso con la calidad y la autenticidad.
                </p>
                <p>
                  A lo largo de estos años, hemos formado una red de más de 30 familias artesanas de diferentes
                  regiones, cada una especializada en técnicas únicas que reflejan la rica diversidad cultural de
                  nuestro país. Juntos, trabajamos para mantener vivas tradiciones centenarias y llevar un pedazo de
                  nuestra cultura a hogares de todo el mundo.
                </p>
              </div>
            </div>
            <div className="history-image-container">
              <img
                src={logo}
                alt="Fundador de Manos Creativas"
                className="history-image"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Proceso Artesanal */}
      <section className="process-section">
        <div className="container">
          <h2 className="section-title">Nuestro Proceso Artesanal</h2>
          <p className="section-description">
            Cada pieza pasa por un cuidadoso proceso que honra las técnicas tradicionales
          </p>

          <div className="process-content">
            <div className="process-steps">
              {proceso.map((paso, index) => (
                <div key={index} className="process-step">
                  <div className="step-number">{index + 1}</div>
                  <div className="step-content">
                    <h3 className="step-title">{paso.title}</h3>
                    <p className="step-description">{paso.description}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="process-image-container">
              <img
                src="https://images.unsplash.com/photo-1610701596007-11502861dcfa"
                alt="Proceso artesanal"
                className="process-image"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default AboutUs