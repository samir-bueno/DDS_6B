from sqlmodel import Session, select
from db.conexcion import db
from db.modelos import Pedidos

def consultarPedidos(cliente_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(Pedidos.cliente_id == cliente_id)
        resultados = sesion.exec(consulta)
        return resultados.all()