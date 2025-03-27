from db.modelos import Clientes, Productos
from app.clientes.registrar import registrar as registrarNuevoCliente
from app.productos.registrar import registrar as registrarNuevoProducto
from app.pedidos.registrar import PedidoARegistrar, registrar as registrarNuevoPedido
from app.clientes.consultar_pedido import consultarPedidos
from app.clientes.consultar_pedido_especifico import consultarPedidoEspecifico
from app.clientes.actualizar_estado_de_pedido import actualizarEstadoPedido, EstadoPedido
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

@app.put("/api/v1/clientes/{cliente_id}/pedidos/{pedido_id}/estado")
def actualizar_estado(cliente_id: str, pedido_id: str, estado_pedido: EstadoPedido):
    estado = estado_pedido.estado  # Obtenemos el estado del cuerpo de la solicitud
    pedido_actualizado = actualizarEstadoPedido(cliente_id, pedido_id, estado)
    
    # Devolvemos el pedido actualizado con su nuevo estado
    return {
        "message": "Estado del pedido actualizado correctamente.",
        "pedido_actualizado": {
            "id": pedido_actualizado.id,
            "estado": pedido_actualizado.estado
        }
    }