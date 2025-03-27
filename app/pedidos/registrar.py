from pydantic import BaseModel
from sqlmodel import Session
from db.modelos import Pedidos, ProductosEnPedidos
from db.conexcion import db

class ProductosEnPedidoRegistrar(BaseModel):
    producto_id: str
    cantidad: int

class PedidoARegistrar(BaseModel):
    cliente_id: str
    productos: list[ProductosEnPedidoRegistrar]

def registrar(pedidoARegistrar: PedidoARegistrar):
    with Session(db) as sesion:
        pedido = Pedidos(cliente_id=pedidoARegistrar.cliente_id)
        sesion.add(pedido)

        for producto in pedidoARegistrar.productos:
            sesion.add(
                ProductosEnPedidos(
                    pedido_id=pedido.id,
                    producto_id=producto.producto_id,
                    cantidad=producto.cantidad
                )
            )

        sesion.commit()
        sesion.refresh(pedido)
    return pedido