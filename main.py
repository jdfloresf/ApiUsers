from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import users, authuser


app = FastAPI()

# Routers
app.include_router(users.user_router)
app.include_router(users.users_router)
app.include_router(authuser.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["root"])
async def root():
    return "Hola xd"


@app.get("/url", tags=["root"])
async def url():
    return {"url": "https://api/v0"}