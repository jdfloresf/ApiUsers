# API Prototipo

Este es un prototipo de API desarrollada con FastAPI. La API está desplegada en [Railway](https://railway.app/) y cuenta con endpoints para gestionar usuarios.

## Estructura del Proyecto

```
├── db              # Contiene la configuración y esquemas de la base de datos
├── routers         # Contiene los archivos de rutas (endpoints)
├── static/images   # Directorio para almacenar imágenes estáticas
├── utils           # Funciones auxiliares y utilidades
├── .gitignore      # Archivos y carpetas que deben ser ignorados por Git
├── main.py         # Archivo principal donde se ejecuta la aplicación FastAPI
├── requirements.txt # Lista de dependencias necesarias para ejecutar la API
```
## Endpoints

### Usuarios

- **GET** `/users/{id}` → Obtiene un usuario por ID.
- **POST** `/users/` → Crea un nuevo usuario.
- **PUT** `/users/` → Actualiza los datos de un usuario.
- **DELETE** `/users/{id}` → Elimina un usuario.

## Tecnologías Utilizadas

- Python
- FastAPI
- Uvicorn
- MongoDB (MongoDB Atlas)
- Railway (para el despliegue)


