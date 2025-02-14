from bson import ObjectId

from db.client import db_client # Conexión a la base de datos
from db.models.user import User # Modelo de usuario definido con Pydantic
from db.schemas.user import user_schema, users_schema # Funciones para formatear datos de MongoDB

from fastapi import APIRouter, HTTPException, status

from typing import List, Optional

from utils.search_user import search_user # Función para buscar usuarios en la base de datos

# Configuración del router para la API de usuarios
router = APIRouter(prefix="/userdb", # Prefijo de la ruta para todas las solicitudes de usuarios
                        tags=["user"],  # Categoría para la documentación de Swagger
                        responses={status.HTTP_404_NOT_FOUND: {"msg":"Not found"}}) # Respuesta estándar para errores 404


@router.get("/", response_model=List[User])
async def users(id: Optional[str] = None):
    """
    Obtiene todos los usuarios o uno en específico si se pasa un ID como Query 
    parameter.
    - Si `id` es proporcionado, retorna una lista con el usuario 
    correspondiente.
    - Si no se proporciona `id`, retorna todos los usuarios registrados en la 
    base de datos.
    """
    
    if id:
        return [search_user("_id", ObjectId(id)) ]   
    return users_schema(db_client.local.users.find())


# Path
@router.get("/{id}")
async def get_user_by_path(id: str):
    """
    Obtiene un usuario por su ID, pasado como parámetro en la URL.
    - Si el usuario existe, lo retorna.
    - Si no existe, devuelve una respuesta de error 404.
    """
    return search_user("_id", ObjectId(id))


# Crear un usuario
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    """
    Crea un nuevo usuario en la base de datos.
    - Verifica si ya existe un usuario con el mismo correo electrónico.
    - Si el usuario ya existe, retorna un error 409 Conflict.
    - Si no existe, lo inserta en la base de datos y lo devuelve.
    """
    
    if type(search_user("email", user.email)) == User:
       raise HTTPException(
           status_code=status.HTTP_409_CONFLICT,
           detail="User with this email already exists") 
    
    user_dict = dict(user)
    del user_dict["id"] # Se elimina el ID para que MongoDB lo genere automáticamente

    # Inserta el usuario y obtiene su ID
    id = db_client.local.users.insert_one(user_dict).inserted_id

    # Obtiene el usuario insertado
    new_user = user_schema(db_client.local.users.find_one({"_id":id}))

    return User(**new_user) # Devuelve el usuario en formato Pydantic

# Actualizar usuario
@router.put("/", response_model=User)
async def update_user(user: User):
    """
    Actualiza los datos de un usuario en la base de datos.
    - Busca al usuario por su ID y reemplaza los datos existentes.
    - Si el usuario no se encuentra, retorna un error 404.
    """

    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")
    
    return search_user("_id", ObjectId(user.id))


# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """
    Elimina un usuario de la base de datos por su ID.
    - Si el usuario existe, lo elimina y retorna un código 204 (sin contenido).
    - Si el usuario no existe, retorna un error indicando que no se encontró.
    """

    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "User not found"}