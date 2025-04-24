"use client"

import { useState, useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import ProductCard from "../components/ProductCard"
import PageHeader from "../components/PageHeader"
import servilleta_bordada from '../imagenes/servilleta.jpg'
import "../hojas-de-estilo/Products.css"

function Products() {
  const [searchParams, setSearchParams] = useSearchParams()
  const categoriaParam = searchParams.get("categoria")
  const [selectedCategory, setSelectedCategory] = useState(categoriaParam || "todos")

  // Actualizar selectedCategory cuando cambia el parámetro de URL
  useEffect(() => {
    setSelectedCategory(categoriaParam || "todos")
  }, [categoriaParam])

  // Datos de ejemplo para productos - Ajustados a 3 por categoría (9 en total)
  const productos = [
    // Cerámica (3 productos)
    {
      id: 1,
      name: "Jarrón de Cerámica Pintado a Mano",
      price: 1200,
      image: "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261",
      category: "Cerámica",
      description: "Jarrón de cerámica pintado a mano con diseños tradicionales de nuestra región.",
      material: "Cerámica",
      origin: "Oaxaca, México",
    },
    {
      id: 6,
      name: "Plato Decorativo de Talavera",
      price: 680,
      image: "https://images.unsplash.com/photo-1603204077779-bed963ea7d0e",
      category: "Cerámica",
      description: "Plato decorativo de Talavera con motivos florales tradicionales pintados a mano.",
      material: "Cerámica de Talavera",
      origin: "Puebla, México",
    },
    {
      id: 8,
      name: "Lámpara de Barro",
      price: 750,
      image: "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15",
      category: "Cerámica",
      description: "Lámpara artesanal de barro negro con patrones calados para efectos de luz.",
      material: "Barro negro",
      origin: "Oaxaca, México",
    },

    // Textiles (3 productos)
    {
      id: 2,
      name: "Tapete Tejido Tradicional",
      price: 850,
      image: "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2",
      category: "Textiles",
      description: "Tapete tejido a mano con lana natural y teñido con tintes vegetales.",
      material: "Lana natural",
      origin: "Chiapas, México",
    },
    {
      id: 7,
      name: "Cojín Bordado a Mano",
      price: 520,
      image: "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace",
      category: "Textiles",
      description: "Cojín con bordado tradicional de motivos florales en hilos de algodón.",
      material: "Algodón 100%",
      origin: "Yucatán, México",
    },
    {
      id: 11,
      name: "Servilletas Bordadas",
      price: 280,
      image: servilleta_bordada,
      category: "Textiles",
      description: "Juego de servilletas con delicados bordados hechos a mano para ocasiones especiales.",
      material: "Lino",
      origin: "Aguascalientes, México",
    },

    // Joyería (3 productos)
    {
      id: 4,
      name: "Collar de Cuentas de Vidrio",
      price: 450,
      image: "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908",
      category: "Joyería",
      description: "Collar artesanal con cuentas de vidrio soplado y plata de diseño prehispánico.",
      material: "Vidrio y plata",
      origin: "Puebla, México",
    },
    {
      id: 10,
      name: "Pulsera de Plata",
      price: 420,
      image: "https://images.unsplash.com/photo-1611652022419-a9419f74343d",
      category: "Joyería",
      description: "Pulsera de plata .925 con diseños inspirados en símbolos prehispánicos.",
      material: "Plata .925",
      origin: "Taxco, México",
    },
    {
      id: 14,
      name: "Aretes de Filigrana",
      price: 290,
      image: "https://images.unsplash.com/photo-1630019852942-f89202989a59",
      category: "Joyería",
      description: "Aretes elaborados con técnica de filigrana en plata formando diseños florales.",
      material: "Plata .925",
      origin: "Oaxaca, México",
    },
  ]

  // Filtrar productos por categoría
  const filteredProducts =
    selectedCategory === "todos"
      ? productos // Ya no necesitamos mezclar los productos
      : productos.filter((product) => product.category.toLowerCase() === selectedCategory.toLowerCase())

  // Función para cambiar la categoría
  const handleCategoryChange = (e) => {
    const categoria = e.target.value
    setSelectedCategory(categoria)

    if (categoria === "todos") {
      setSearchParams({})
    } else {
      setSearchParams({ categoria })
    }
  }

  return (
    <div className="products-page">
      <PageHeader
        title="Nuestros Productos"
        description="Descubre nuestra colección de artesanías únicas hechas a mano"
      />

      <section className="products-section">
        <div className="container">
          {/* Filtros */}
          <div className="filters">
            <div className="filter-label">Categoría:</div>
            <select className="category-select" value={selectedCategory} onChange={handleCategoryChange}>
              <option value="todos">Todos</option>
              <option value="cerámica">Cerámica</option>
              <option value="textiles">Textiles</option>
              <option value="joyería">Joyería</option>
            </select>
          </div>

          {/* Productos */}
          <div className="products-grid">
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default Products