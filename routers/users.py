from fastapi import APIRouter, HTTPException
from models.user import User

user_router = APIRouter(prefix="/user", 
                        tags=["user"],
                        responses={404: {"msg":"Not found"}})

users_router = APIRouter(prefix="/users", 
                         tags=["user"],
                         responses={404: {"msg":"Not found"}})



users_list = [User(id=1, name="Jonathan", surname="Jhon", age=24),
              User(id=2, name="Juan", surname="Juan", age=19),
              User(id=3, name="Alejandro",surname="Ale", age=45)]


@users_router.get("")
async def users():
    return users_list


# Path
@user_router.get("/{id}")
async def user(id: int):
    return search_user(id)


# Query
@user_router.get("/")
async def user(id: int):
    return search_user(id)
    

# Agregar un usuario
@user_router.post("/", status_code=201, response_model=User)
async def user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=204,detail="User alredy exist") 
    
    users_list.user_routerend(user)
    return user


@user_router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "User not found"}
    return user


@user_router.delete("/{id}")
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"msg": "User deleted"}



def search_user(id: int):
    try: 
        users = filter(lambda user: user.id == id, users_list)
        return list(users)[0]
    except:
        return {"error": "User not found"}