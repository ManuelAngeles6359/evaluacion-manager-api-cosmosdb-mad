from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from database import container_usuarios, container_proyectos
from models import Usuario, Proyecto
from azure.cosmos import exceptions
from datetime import datetime


app = FastAPI(title='API de Gestion de Usuario y sus proyectos')

#### Endpoint de Eventos

@app.get("/")
def home():
    return "Hola Mundo"


# Crear usuario
@app.post("/usuarios/", response_model=Usuario, status_code=201)
def create_usuario(usuario: Usuario):
    try:
        container_usuarios.create_item(body=usuario.dict())
        return usuario
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El usuario con este ID ya existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))



# Listar usuarios
@app.get("/usuarios/", response_model=List[Usuario])
def list_usuarios():
    
    query = "SELECT * FROM c WHERE 1=1"
    items = list(container_usuarios.query_items(query=query, enable_cross_partition_query=True))
    return items


# Actualizar usuario
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id: str, updated_usuario: Usuario):

    try:

        existing_usuario = container_usuarios.read_item(item=usuario_id, partition_key= usuario_id)
        existing_usuario.update(updated_usuario.dict(exclude_unset=True))
        
        container_usuarios.replace_item(item= usuario_id, body= existing_usuario)
        
        return existing_usuario

    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado.')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))  


# Eliminar usuario
@app.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: str):
    try:
        container_usuarios.delete_item(item=usuario_id, partition_key=usuario_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encotrado.')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Crear proyecto
@app.post("/proyectos/", response_model=Proyecto, status_code=201)
def create_proyecto(proyecto: Proyecto):
    try:
        
        existing_usuario = container_usuarios.read_item(item=proyecto.id_usuario, partition_key=proyecto.id_usuario)        
        container_proyectos.create_item(body=proyecto.dict())
        return proyecto
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encotrado.')
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El proyecto con este ID ya existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Listar los proyectos
@app.get("/proyectos/", response_model=List[Proyecto])
def list_proyectos():
    
    query = "SELECT * FROM c WHERE 1=1"
    items = list(container_proyectos.query_items(query=query, enable_cross_partition_query=True))
    return items



# Actualizar proyecto
@app.put("/proyectos/{proyecto_id}", response_model=Proyecto)
def update_proyecto(proyecto_id: str, updated_proyecto: Proyecto):

    try:
        
        mensaje_error = 'Usuario no encontrado.'
        existing_usuario = container_usuarios.read_item(item=updated_proyecto.id_usuario, partition_key=updated_proyecto.id_usuario)
        
        mensaje_error = 'Proyecto no encontrado.'
        existing_proyecto = container_proyectos.read_item(item=proyecto_id, partition_key= proyecto_id)    
        existing_proyecto.update(updated_proyecto.dict(exclude_unset=True))    
        
        container_proyectos.replace_item(item= proyecto_id, body= existing_proyecto)

        return existing_proyecto

    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail=mensaje_error)
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))  



# Eliminar proyecto
@app.delete("/proyectos/{proyecto_id}", status_code=204)
def delete_proyecto(proyecto_id: str):
    try:
        container_proyectos.delete_item(item=proyecto_id, partition_key=proyecto_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encotrado.')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Listar proyectos por usuario
@app.get("/usuarios/{usuario_id}/proyectos/", response_model=List[Proyecto])
def list_proyectos(usuario_id: str):
    
    try:

        existing_usuario = container_usuarios.read_item(item=usuario_id, partition_key=usuario_id)

        query = "SELECT * FROM c WHERE c.id_usuario = '" + usuario_id + "'"
        items = list(container_proyectos.query_items(query=query, enable_cross_partition_query=True))
        return items 

    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado.')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))  