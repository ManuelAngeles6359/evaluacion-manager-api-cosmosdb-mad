from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
 

class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str= Field(..., example='Manuel')
    email: EmailStr = Field(..., example='manuel.angeles@example.com')
    edad: int = Field(..., example=25)


class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str = Field(..., example='Proyecto 01')
    descripcion: str = Field(..., example='Descripcion de Proyecto 01')
    id_usuario: str = Field(..., example='u1')
    fecha_creacion: str = Field(..., example='2024-11-01T19:00:00Z')