from fastapi import APIRouter, HTTPException, status

from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema

from bson import ObjectId

router = APIRouter(prefix="/userdb", 
                        tags=["user"],
                        responses={status.HTTP_404_NOT_FOUND: {"msg":"Not found"}})

users_list = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


# Path
@router.get("/{id}")
async def get_user_by_path(id: str):
    return search_user("_id", ObjectId(id))


# Query
@router.get("/")
async def get_user_by_query(id: str):
    return search_user("_id", ObjectId(id))
    

# Agregar un usuario
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
       raise HTTPException(
           status_code=status.HTTP_409_CONFLICT,
           detail="User with this email already exists") 
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id}))

    return User(**new_user)


@router.put("/", response_model=User)
async def update_user(user: User):

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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "User not found"}



def search_user(key: str, value):
    try: 
        user = user_schema(db_client.local.users.find_one({key: value}))
        return User(**user)
    except:
        return {"error": "User not found"}