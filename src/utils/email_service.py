# src/utils/email_service.py
# Servicio de correo simple: usa SMTP si hay configuración, o simula imprimiendo en consola.

import os
import smtplib
from email.message import EmailMessage

# Carga de configuración SMTP desde variables de entorno (si existen)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM")  # Remitente (ej: "no-reply@tu-dominio.com")


def _smtp_configured() -> bool:
    return all([SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_FROM])


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Envía un correo: si hay SMTP configurado usa envío real; de lo contrario simula.
    """
    # Simulación si no hay SMTP configurado
    if not _smtp_configured():
        print("\n--- Simulando envío de correo ---")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("--- Fin simulación ---\n")
        return True

    try:
        msg = EmailMessage()
        msg["From"] = SMTP_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)

        return True
    except Exception as e:
        print(f"Error al enviar correo real: {e}")
        return False
