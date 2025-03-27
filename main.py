from db.modelos import Clientes, Productos
from app.clientes.registrar import registrar as registrarNuevoCliente
from app.productos.registrar import registrar as registrarNuevoProducto
from app.pedidos.registrar import PedidoARegistrar, registrar as registrarNuevoPedido
from app.clientes.consultar_pedido import consultarPedidos
from app.clientes.consultar_pedido_especifico import consultarPedidoEspecifico
from app import app 

@app.get("/api/saludo")
def read_root():
    return {"Hello": "World"}

@app.post("/api/v1/clientes")
def post_clientes(cliente: Clientes):
    return registrarNuevoCliente(cliente)

@app.post("/api/v1/productos")
def post_productos(producto: Productos):
    return registrarNuevoProducto(producto)

@app.post("/api/v1/pedidos")
def post_pedidos(pedido: PedidoARegistrar):
    return registrarNuevoPedido(pedido)

@app.get("/api/v1/clientes/{cliente_id}/pedidos")
def get_pedidos(cliente_id: str):
    pedidos = consultarPedidos(cliente_id)
    return {"pedidos": pedidos}

@app.get("/api/v1/clientes/{cliente_id}/pedidos/{pedido_id}/estado")
def get_pedidos_especifico(cliente_id: str, pedido_id: str):
    pedido = consultarPedidoEspecifico(cliente_id, pedido_id)
    return {"id": pedido.id, "pedidos": pedido.estado}