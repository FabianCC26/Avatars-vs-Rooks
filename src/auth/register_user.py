import re
import hashlib
import requests
from DBconfig.firebase_config import db, API_KEY


# VALIDACIÓN DE DATOS DE USUARIO

def validar_datos_usuario(data: dict) -> tuple[bool, str]:
    """
    Verifica que los datos del usuario sean válidos.
    
    Requisitos:
    - role: 'player' o 'admin'
    - username: 3-20 caracteres alfanuméricos o guiones bajos
    - password: entre 6 y 12 caracteres, al menos una mayúscula y un carácter especial
    - email válido
    - Si role = 'admin' → requiere name, lastname, nationality
    """

    if "role" not in data or data["role"] not in ["player", "admin"]:
        return False, "Rol inválido. Debe ser 'player' o 'admin'."

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", data.get("username", "")):
        return False, "Nombre de usuario inválido. Use 3-20 caracteres alfanuméricos o '_' ."

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email", "")):
        return False, "Correo electrónico inválido."

    password = data.get("password", "")
    if len(password) < 6 or len(password) > 12:
        return False, "La contraseña debe tener entre 6 y 12 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"[^a-zA-Z0-9]", password):
        return False, "La contraseña debe contener al menos un carácter especial."

    # Validaciones específicas del administrador
    if data["role"] == "admin":
        for field in ["name", "lastname", "nationality"]:
            if not data.get(field):
                return False, f"El campo '{field}' es obligatorio para administradores."

    return True, "Validación exitosa."


# MÉTODOS AUXILIARES

def hash_password(password: str) -> str:
    """
    Cifra la contraseña con SHA-256 antes de guardarla.
    Esto evita almacenar texto plano en Firestore.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def registrar_en_firebase_auth(email: str, password: str) -> tuple[bool, str | None]:
    """
    Crea un nuevo usuario en Firebase Authentication mediante la REST API.
    Devuelve (True, uid) si el registro fue exitoso.
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return True, data.get("localId")  # UID del usuario en Auth
    else:
        return False, f"Error de Firebase Auth: {response.json()}"


# REGISTRO DE USUARIO EN FIREBASE

def registrar_usuario(data: dict) -> tuple[bool, str]:
    """
    Registra un nuevo usuario en la colección 'users' de Firestore y en Firebase Authentication.
    Usa el 'username' como ID del documento para evitar duplicados.
    """

    # Validar datos antes de registrar
    valid, msg = validar_datos_usuario(data)
    if not valid:
        return False, msg

    try:
        username = data["username"].strip().lower()
        email = data["email"].strip().lower()
        password = data["password"]

        user_ref = db.collection("users").document(username)
        existing_doc = user_ref.get()

        # Verificar si ya existe el usuario
        if existing_doc.exists:
            return False, f"El nombre de usuario '{username}' ya existe."

        # Verificar si el correo está registrado en otro usuario
        existing_email = list(db.collection("users").where("email", "==", email).stream())
        if existing_email:
            return False, f"El correo '{email}' ya está registrado."

        # Registrar el usuario en Firebase Authentication
        auth_success, auth_result = registrar_en_firebase_auth(email, password)
        if not auth_success:
            return False, f"No se pudo registrar en Firebase Auth: {auth_result}"

        uid = auth_result

        # Cifrar la contraseña antes de guardar en Firestore
        hashed_password = hash_password(password)

        # Crear estructura estandarizada de usuario
        user_data = {
            "role": data["role"],
            "username": username,
            "email": email,
            "password": hashed_password,  # Contraseña cifrada
            "uid": uid
        }

        # Agregar campos de admin si aplica
        if data["role"] == "admin":
            user_data.update({
                "name": data["name"],
                "lastname": data["lastname"],
                "nationality": data["nationality"]
            })

        # Registrar usuario (documento con ID = username)
        user_ref.set(user_data)

        return True, f"Usuario '{username}' registrado correctamente."

    except Exception as e:
        return False, f"Error al registrar usuario: {e}"
