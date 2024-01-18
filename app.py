from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json

# Crear una instancia de FastAPI
app = FastAPI()

# Definir el modelo de datos usando Pydantic
class User(BaseModel):
    name: str  # Nombre del usuario, debe ser un string
    email: str  # Correo electrónico del usuario, debe ser un string

# Definir un endpoint para la raíz con método GET
@app.get("/")
def home():
    # Retorna un simple mensaje de texto
    return 'Hola mundo'

def save_user(user_data):
    # Nombre del archivo donde se guardarán los datos de los usuarios
    file_name = 'users_1.json'

    try:
        # Intentar abrir el archivo existente para leer los usuarios ya guardados
        with open(file_name, 'r') as file:
            # Cargar los datos del archivo JSON en la variable 'users'
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o hay un error al leer el JSON,
        # se inicializa una lista vacía para los usuarios
        users = []

    # Añadir el nuevo usuario a la lista de usuarios
    users.append(user_data)

    # Guardar la lista actualizada de usuarios en el archivo JSON
    with open(file_name, 'w') as file:
        # json.dump escribe la lista de usuarios en el archivo,
        # 'indent=4' se usa para formatear el archivo de manera legible
        json.dump(users, file, indent=4)

# Definición del endpoint para agregar usuarios con un método POST
@app.post("/users")
def add_user(user: User):
    # 'user: User' indica que los datos de la solicitud deben coincidir con el modelo 'User'
    # 'user.dict()' convierte los datos del usuario a un diccionario
    user_data = user.dict()

    # Llamar a la función 'save_user' para guardar los datos del usuario
    save_user(user_data)

    # Retornar una respuesta indicando que el usuario fue agregado exitosamente
    return {"message": "Usuario agregado exitosamente", "user": user_data}


# Ejecutar la aplicación usando Uvicorn
if __name__ == "__main__":
    # host="0.0.0.0" permite acceder al servidor desde cualquier dirección
    # port=8000 es el puerto en el que se iniciará el servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)