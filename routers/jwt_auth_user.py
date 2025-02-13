from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from  passlib.context import CryptContext

from models.authuser import AuthUser, UserDB

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "342f068d6ee5269b4790fd6b10a1f5a1767a96eaac27fbe942c1ba5b00b5ee6e"

router = APIRouter(tags=["JWT"], 
                   responses={404: {"msg":"Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="/jwt/login")

crypt = CryptContext(schemes=["bcrypt"])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) if username in users_db else None
    
def search_user(username: str):
    if username in users_db:
        return AuthUser(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid or expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = search_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# Criterio de dependencia
async def current_user(user: AuthUser = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authentication invalid")

    return user
    
@router.post("/jwt/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User or password invalids")
    
    user = search_user_db(form.username)

    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User or password invalids")


    access_token = {"sub":user.username, 
                    "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def profile(user: AuthUser = Depends(current_user)):
    return user



users_db = {
    "jonathan": {
        "username": "jonathan",
        "full_name": "Jonathan Flores",
        "email": "jonathan@asdrome.com",
        "disabled": False,
        "password": "$2a$12$iJnKVs7hWNyvRXubDQ2TCeg0O8qc6EY0Zq0pnBbOgMoM5IFftVEOa"
    },
    "asdrome": {
        "username": "asdrome",
        "full_name": "Asdrome drome",
        "email": "asdrome@asdrome.com",
        "disabled": True,
        "password": "$2a$12$f0fmvyTJURX06J4JVUTer.ucPScexJo6aW/WJyhJVGDX2Js6ni0he"
    }
}
