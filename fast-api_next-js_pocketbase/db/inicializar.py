from sqlmodel import SQLModel
from db.conexcion import db

def crearTablas():
    SQLModel.metadata.create_all(db)