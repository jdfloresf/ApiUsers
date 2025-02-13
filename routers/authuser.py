from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.authuser import AuthUser, UserDB

router = APIRouter(tags=["AuthUser"], 
                   responses={404: {"msg":"Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return AuthUser(**users_db[username])


# Criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User inactive",
            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authentication invalid")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User or password invalids")
    
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User or password invalids")

    return {"access_token": user.username , "token_type": "bearer"}

@router.get("/users/profile")
async def profile(user: AuthUser = Depends(current_user)):
    return user


users_db = {
    "jonathan": {
        "username": "jonathan",
        "full_name": "Jonathan Flores",
        "email": "jonathan@asdrome.com",
        "disabled": False,
        "password": "123456"
    },
    "asdrome": {
        "username": "asdrome",
        "full_name": "Asdrome drome",
        "email": "asdrome@asdrome.com",
        "disabled": True,
        "password": "654321"
    }
}