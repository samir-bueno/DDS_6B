from sqlmodel import Session, select
from db.conexcion import db
from db.modelos import Pedidos

def consultarPedidoEspecifico(cliente_id: str, pedido_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(
            (Pedidos.cliente_id == cliente_id) & (Pedidos.id == pedido_id)
        )
        resultado = sesion.exec(consulta).first()
        return resultado