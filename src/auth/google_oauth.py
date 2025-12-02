import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport import requests
from src.config import settings


def login_with_google():
    """
    Lanza la ventana de login de Google,
    obtiene credenciales OAuth reales,
    valida el id_token y devuelve los datos del usuario.
    """
    # Crear flujo OAuth usando CLIENT_ID y CLIENT_SECRET del .env
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["openid", "email", "profile"]
    )

    # Abre el navegador para iniciar sesión
    creds = flow.run_local_server(port=0)

    # Extraer y validar id_token
    token = creds.id_token

    try:
        info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except Exception as e:
        print("Error verificando token:", e)
        return None

    # Datos que necesitamos
    user_data = {
        "email": info.get("email"),
        "google_id": info.get("sub"),
        "name": info.get("name"),
        "picture": info.get("picture"),
    }

    return user_data
