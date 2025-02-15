from db.schemas.user import user_schema
from db.models.user import User
from db.client import db_client

from typing import Optional

def search_user(key: str, value) -> Optional[User]:
    """
    Busca un usuario en la base de datos por una clave y un valor específico.

    :param key: Campo por el cual se quiere buscar (por ejemplo, "_id" o "email").
    :param value: Valor que se desea buscar en la base de datos.
    :return: Una instancia de User si el usuario existe, de lo contrario None.
    """
    user = db_client.users.find_one({key: value})

    if not user:
        return None

    try: 
        return User(**user_schema(user))
    except(TypeError, AttributeError):
        return None