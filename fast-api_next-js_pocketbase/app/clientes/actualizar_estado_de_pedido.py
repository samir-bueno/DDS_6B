from pydantic import BaseModel
from sqlmodel import Session, update, select
from db.conexcion import db
from db.modelos import Pedidos

class EstadoPedido(BaseModel):
    estado: str

def actualizarEstadoPedido(cliente_id: str, pedido_id: str, estado: str):
    with Session(db) as sesion:
        sesion.exec(
            update(Pedidos)
            .where(Pedidos.cliente_id == cliente_id, Pedidos.id == pedido_id)
            .values(estado=estado)
        )
        sesion.commit()
        
        pedido_actualizado = sesion.exec(
            select(Pedidos).where(Pedidos.cliente_id == cliente_id, Pedidos.id == pedido_id)
        ).first()
    
    return pedido_actualizado
