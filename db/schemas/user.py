from typing import List, Dict

def user_schema(user: dict) -> dict:
    """
    Convierte un documento de usuario de MongoDB a un formato legible por la API.

    :param user: Diccionario que representa un usuario en la base de datos.
    :return: Diccionario con los datos del usuario, donde '_id' se convierte a 'id'.
    """
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}

def users_schema(users: List[dict]) -> List[Dict]:
    """
    Convierte una lista de documentos de MongoDB a una lista de diccionarios en formato API.

    :param users: Lista de diccionarios representando usuarios en la base de datos.
    :return: Lista de diccionarios con los datos de los usuarios.
    """
    return [user_schema(user) for user in users]