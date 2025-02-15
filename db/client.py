import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
# Conexión a DB local
# db_client = MongoClient().local

#Conexión a DB prod

URI = os.getenv("URI")

if not URI:
    raise ValueError("URI no está definido en el archivo .env")

db_client = MongoClient(URI).user
