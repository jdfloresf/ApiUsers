from pydantic import BaseModel

# Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int