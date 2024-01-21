from flask import Flask, request
import json

app = Flask(__name__)

def save_user(user_data):
    # Nombre del archivo donde se guardarán los datos de los usuarios
    file_name = 'users_3.json'

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

@app.route("/users", methods=["POST"])
def add_user():
    user_data = request.get_json()

    # Llamar a la función 'save_user' para guardar los datos del usuario
    save_user(user_data)

    # Retornar una respuesta indicando que el usuario fue agregado exitosamente
    return {"message": "Usuario agregado exitosamente", "user": user_data}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
