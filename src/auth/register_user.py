import re
from DBconfig.firebase_config import db


# VALIDACIÓN DE DATOS DE USUARIO


def validar_datos_usuario(data: dict) -> tuple[bool, str]:
    """
    Verifica que los datos del usuario sean válidos.
    
    Requisitos:
    - role: 'player' o 'admin'
    - username: 3-20 caracteres alfanuméricos o guiones bajos
    - password: mínimo 6 caracteres
    - email válido
    - Si role = 'admin' → requiere name, lastname, nationality
    """

    if "role" not in data or data["role"] not in ["player", "admin"]:
        return False, "Rol inválido. Debe ser 'player' o 'admin'."

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", data.get("username", "")):
        return False, "Nombre de usuario inválido. Use 3-20 caracteres alfanuméricos o '_' ."

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email", "")):
        return False, "Correo electrónico inválido."

    if len(data.get("password", "")) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."

    # Validaciones específicas del administrador
    if data["role"] == "admin":
        for field in ["name", "lastname", "nationality"]:
            if not data.get(field):
                return False, f"El campo '{field}' es obligatorio para administradores."

    return True, "Validación exitosa."



# REGISTRO DE USUARIO EN FIREBASE


def registrar_usuario(data: dict) -> tuple[bool, str]:
    """
    Registra un nuevo usuario en la colección 'users' de Firestore.
    Usa el 'username' como ID del documento para evitar duplicados.

    """

    # Validar datos antes de registrar
    valid, msg = validar_datos_usuario(data)
    if not valid:
        return False, msg

    try:
        username = data["username"].strip().lower()  # normalizamos el username
        email = data["email"].strip().lower()

        user_ref = db.collection("users").document(username)
        existing_doc = user_ref.get()

        # Verificar si ya existe el usuario
        if existing_doc.exists:
            return False, f"El nombre de usuario '{username}' ya existe."

        # Verificar si el correo está registrado en otro usuario
        existing_email = list(db.collection("users").where("email", "==", email).stream())
        if existing_email:
            return False, f"El correo '{email}' ya está registrado."

        # Crear estructura estandarizada de usuario
        user_data = {
            "role": data["role"],
            "username": username,
            "email": email,
            "password": data["password"],  # En el futuro crear un metodo de cifrado 
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
