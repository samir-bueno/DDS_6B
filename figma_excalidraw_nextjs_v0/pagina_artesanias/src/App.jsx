import { BrowserRouter as Router, Routes, Route } from "react-router-dom"

// Componentes
import Header from "./components/Header"
import Footer from "./components/Footer"
import Home from "./pages/Home"
import Products from "./pages/Products"
import AboutUs from "./pages/AboutUs"
import ScrollToTop from "./components/ScrollToTop"

// Estilos
import "./hojas-de-estilo/App.css"

function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/productos" element={<Products />} />
            <Route path="/sobre-nosotros" element={<AboutUs />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App