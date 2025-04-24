import "../hojas-de-estilo/ProductCard.css"

function ProductCard({ product }) {
  // Verificar que product y price existan para evitar errores
  const price = product && product.price ? product.price.toLocaleString() : "Precio no disponible"

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img src={product.image || "/placeholder.svg"} alt={product.name} className="product-image" />
        <div className="category-badge">
          <span className="category-text">{product.category}</span>
        </div>
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <div className="product-footer">
          <span className="product-price">${price}</span>
        </div>
        <p className="product-description">{product.description}</p>
      </div>
    </div>
  )
}

export default ProductCard