import warnings
warnings.filterwarnings("ignore")  # Ignora los warnings de Firestore
from DBconfig.firebase_config import *
import requests


def login_por_username(username, password):     # Función de login por username
    """
    Valida un usuario en Firestore por username y contraseña usando Firebase Auth REST API
    """
    print(f"\n Buscando usuario '{username}' en Firestore...")

    usuarios_ref = db.collection("users")
    query = usuarios_ref.where("username", "==", username).stream()
    usuario_encontrado = None

    for doc in query:
        usuario_encontrado = doc
        print("Datos obtenidos de Firestore:", doc.to_dict())
        break

    if not usuario_encontrado:
        print("Usuario no encontrado en la base de datos.")
        return None

    # Obtener el email para autenticación
    email = usuario_encontrado.to_dict().get("email")
    if not email:
        print("Usuario sin email asociado, no se puede autenticar.")
        return None

    print(f"Email usado para autenticación: {email}")

    # Validar contraseña con Firebase Auth REST API
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Inicio de sesión exitoso para {username}")
        return usuario_encontrado.to_dict()
    else:
        print("Contraseña incorrecta o error de autenticación:", response.json())
        return None