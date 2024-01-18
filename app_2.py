from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json

# Crear una instancia de FastAPI
app = FastAPI()

# Definimos el modelo de datos para los usuarios
class User(BaseModel):
    """
    Modelo de datos para los usuarios.

    Atributos:
        id: Identificador único para cada usuario.
        name: Nombre del usuario.
        email: Email del usuario.
    """
    id: int       
    name: str    
    email: str   

# Definimos el modelo de datos para el ID de usuario
class User_ID(BaseModel):
    """
    Modelo de datos para el ID de usuario.

    Atributos:
        id: Identificador único para cada usuario.
    """
    id: int

# Función para guardar los usuarios en un archivo JSON
def save_users(users):
    """
    Guarda los usuarios en un archivo JSON.

    Args:
        users: Lista de usuarios.
    """
    with open('users_2.json', 'w') as file:
        json.dump(users, file, indent=4)

# Función para actualizar los datos de un usuario
def update_user_data(user_id, new_data):
    """
    Actualiza los datos de un usuario.

    Args:
        user_id: Identificador único del usuario.
        new_data: Nuevos datos del usuario.

    Returns:
        True si el usuario fue actualizado exitosamente, False en caso contrario.
    """
    try:
        with open('users_2.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for user in users:
        if user.get("id") == user_id:
            user.update(new_data)
            save_users(users)
            return True

    return False

# Función para eliminar los datos de un usuario
def delete_user_data(user_id):
    """
    Elimina los datos de un usuario.

    Args:
        user_id: Identificador único del usuario.

    Returns:
        True si el usuario fue eliminado exitosamente, False en caso contrario.
    """
    try:
        with open('users_2.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    users = [user for user in users if user.get("id") != user_id]
    save_users(users)
    return True

# Definir un endpoint para la raíz con método GET
@app.get("/")
def home():
    """
    Ruta raíz de la aplicación.

    Returns:
        Un mensaje de bienvenida.
    """
    return 'Hola mundo'

# Definición del endpoint para agregar usuarios con un método POST
@app.post("/users")
def add_user(user: User):
    """
    Ruta para agregar un nuevo usuario.

    Args:
        user: Objeto con los datos del usuario.

    Returns:
        Un mensaje de confirmación y los datos del usuario agregado.
    """
    user_data = user.dict()
    try:
        with open('users_2.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    # Verificar si el id del usuario ya existe
    if any(u['id'] == user.id for u in users):
        raise HTTPException(status_code=400, detail="El ID del usuario ya existe")

    users.append(user_data)
    save_users(users)
    return {"message": "Usuario agregado exitosamente", "user": user_data}

# Ruta para actualizar los datos de un usuario
@app.put("/put_users")
def update_user(user: User):
    """
    Ruta para actualizar los datos de un usuario.

    Args:
        user: Objeto con los datos del usuario.

    Returns:
        Un mensaje de confirmación y los datos del usuario actualizado.
    """
    user_data = user.dict()
    user_id = user_data["id"]
    if update_user_data(user_id, user_data):
        return {"message": "Usuario actualizado exitosamente", "user_id": user_id, "user": user_data}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Ruta para eliminar los datos de un usuario
@app.delete("/delete_users")
def delete_user(user: User_ID):
    """
    Ruta para eliminar los datos de un usuario.

    Args:
        user: Objeto con el ID del usuario.

    Returns:
        Un mensaje de confirmación y el ID del usuario eliminado.
    """
    user_data = user.dict()
    user_id = user_data["id"]
    if delete_user_data(user_id):
        return {"message": "Usuario eliminado exitosamente", "user_id": user_id}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Ejecutar la aplicación usando Uvicorn
if __name__ == "__main__":
    # host="0.0.0.0" permite acceder al servidor desde cualquier dirección
    # port=8000 es el puerto en el que se iniciará el servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)

