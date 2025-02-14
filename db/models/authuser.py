from pydantic import BaseModel

# Entidad User

class AuthUser(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(AuthUser):
    password: str