from typing import Optional
from pydantic import BaseModel, EmailStr

# Modelo de usuario (estructura de datos esperada en la API)
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr