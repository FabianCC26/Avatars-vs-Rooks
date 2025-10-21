import requests
from src.auth.login_user import *


def enviar_password_recovery(email):    # Función para enviar correo de restablecimiento
    """
    Envía un correo de restablecimiento de contraseña al email dado.
    """
    print(f"📧 Enviando correo de restablecimiento a {email}...")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"✅ Correo de restablecimiento enviado correctamente a {email}")
    else:
        print("⚠️ Error al enviar correo:", response.json())


def restablecer_password_por_username(username):    # Función para restablecer contraseña por username
    """
    Busca el email del username en Firestore y pregunta si quiere enviar el correo de recuperación.
    """
    print(f"\n🔍 Buscando usuario '{username}' en Firestore...")

    usuarios_ref = db.collection("users")
    query = usuarios_ref.where("username", "==", username).stream()
    usuario_encontrado = None

    for doc in query:
        usuario_encontrado = doc
        datos_usuario = doc.to_dict()
        print("📄 Datos obtenidos de Firestore:", datos_usuario)
        break

    if not usuario_encontrado:
        print("❌ Usuario no encontrado en Firestore")
        return

    email = datos_usuario.get("email")
    if not email:
        print("❌ Usuario no tiene email asociado")
        return

    opcion = input("¿Desea enviar un correo para restablecer la contraseña? (s/n): ").lower()
    if opcion == "s":
        enviar_password_recovery(email)
    else:
        print("❌ No se enviará correo de recuperación.")


if __name__ == "__main__":      # Prueba desde consola
    username = input("Ingrese el username para recuperar contraseña: ")
    restablecer_password_por_username(username)
