import os
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import users_db


app = FastAPI()

# Routers
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/url", tags=["root"])
async def url():
    return {"message": "API is running on Railway!"}

if __name__ == "__main__":
    # Obtener el puerto asignado por Railway o usar 8000 como valor por defecto
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)