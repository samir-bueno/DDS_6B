from contextlib import asynccontextmanager
from fastapi import FastAPI

from db.inicializar import crearTablas

@asynccontextmanager
async def cicloApp(_):
    print("Inicio de la Aplicacion")
    crearTablas()
    yield
    print("Fin de la Aplicacion")

app = FastAPI(lifespan=cicloApp)