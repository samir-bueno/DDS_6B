import "../hojas-de-estilo/PageHeader.css"

function PageHeader({ title, description }) {
  return (
    <section className="page-header">
      <div className="container">
        <h1 className="page-header-title">{title}</h1>
        {description && <p className="page-header-description">{description}</p>}
      </div>
    </section>
  )
}

export default PageHeader