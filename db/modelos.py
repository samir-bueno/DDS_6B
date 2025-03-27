from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import uuid4


class Clientes(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    create_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default_factory=datetime.now)
    nombre: str
    apellido: str

class Pedidos(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    create_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default_factory=datetime.now)
    cliente_id: str = Field(foreign_key="clientes.id")
    estado: str = Field(default="pendiente") #pendiente, en proceso, entregado

class Productos(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    create_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default_factory=datetime.now)
    descripcion: str

class ProductosEnPedidos(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    create_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default_factory=datetime.now)
    pedido_id: str = Field(foreign_key="pedidos.id")
    producto_id: str = Field(foreign_key="productos.id")
    cantidad: int
