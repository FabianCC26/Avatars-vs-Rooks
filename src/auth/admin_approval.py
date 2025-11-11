# Módulo de aprobación de cuentas de administrador
# - Crea solicitudes de aprobación
# - Envía correos a administradores existentes
# - Permite aprobar por token desde el cliente (panel admin) o herramienta interna

import secrets
from datetime import datetime, timezone
from DBconfig.firebase_config import db
from src.utils.email_service import send_email  # Se asume que existe una función send_email(to, subject, body)


def _admin_email_list() -> list[str]:
    """
    Obtiene la lista de correos de administradores aprobados.
    """
    emails = []
    admins = db.collection("users").where("role", "==", "admin").where("approved", "==", True).stream()
    for doc in admins:
        data = doc.to_dict()
        email = data.get("email")
        if email:
            emails.append(email)
    return emails


def create_admin_approval_request(target_username: str, target_email: str, target_display: str, nationality: dict):
    """
    Crea un documento de solicitud de aprobación en 'admin_approvals' y notifica a los administradores.
    """
    token = secrets.token_urlsafe(32)
    req_ref = db.collection("admin_approvals").document(token)

    payload = {
        "token": token,
        "target_username": target_username,
        "target_email": target_email,
        "target_display": target_display,
        "nationality": nationality,
        "status": "pending",  # 'pending' | 'approved' | 'rejected'
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "approved_by": None,
        "approved_at": None,
        "rejected_by": None,
        "rejected_at": None,
    }
    req_ref.set(payload)

    # Enviar correos a administradores
    to_list = _admin_email_list()
    if not to_list:
        return  # No hay admins para aprobar; quedará pendiente hasta que exista alguno

    subject = "Avatars vs Rooks: nueva solicitud de administrador"
    # El enlace es informativo; se puede usar el token dentro del panel admin del juego
    body = (
        f"Se solicitó acceso de administrador.\n\n"
        f"Usuario: {target_username}\n"
        f"Nombre: {target_display}\n"
        f"Nacionalidad: {nationality}\n"
        f"Correo: {target_email}\n\n"
        f"Token de aprobación: {token}\n"
        f"Instrucciones: Ingrese al panel de administradores del juego y apruebe esta solicitud usando el token.\n"
    )
    for to in to_list:
        try:
            send_email(to, subject, body)
        except Exception:
            pass  # Evitar que un fallo de envío interrumpa el flujo


def approve_admin_by_token(token: str, approver_username: str) -> tuple[bool, str]:
    """
    Aprueba una solicitud por token. Debe llamarse desde un flujo donde 'approver_username'
    es un administrador aprobado. Devuelve (ok, mensaje).
    """
    # Verifica que quien aprueba sea admin aprobado
    approver_doc = db.collection("users").document(approver_username.lower()).get()
    if not approver_doc.exists:
        return False, "Aprobador no existe."
    approver = approver_doc.to_dict()
    if approver.get("role") != "admin" or not approver.get("approved", False):
        return False, "Solo un administrador aprobado puede aprobar solicitudes."

    req_doc = db.collection("admin_approvals").document(token).get()
    if not req_doc.exists:
        return False, "Token inválido o inexistente."

    req = req_doc.to_dict()
    if req.get("status") != "pending":
        return False, "Esta solicitud ya fue procesada."

    target_username = req["target_username"]
    user_ref = db.collection("users").document(target_username)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return False, "Usuario objetivo no existe."

    # Aprobar: marcar usuario como admin aprobado
    user_ref.update({
        "role": "admin",
        "approved": True,
        "approved_by": approver_username,
        "approved_at": datetime.now(timezone.utc).isoformat()
    })

    # Marcar solicitud como aprobada
    db.collection("admin_approvals").document(token).update({
        "status": "approved",
        "approved_by": approver_username,
        "approved_at": datetime.now(timezone.utc).isoformat()
    })

    # Aviso (opcional): notificar al usuario objetivo por correo
    try:
        subject = "Avatars vs Rooks: solicitud de administrador aprobada"
        body = (
            f"Hola {target_username},\n\n"
            f"Tu solicitud para acceder como administrador ha sido aprobada por {approver_username}.\n"
            f"Ya puedes iniciar sesión con privilegios de administrador."
        )
        send_email(req["target_email"], subject, body)
    except Exception:
        pass

    return True, "Solicitud aprobada correctamente."


def reject_admin_by_token(token: str, approver_username: str) -> tuple[bool, str]:
    """
    Rechaza una solicitud por token (opcional).
    """
    approver_doc = db.collection("users").document(approver_username.lower()).get()
    if not approver_doc.exists:
        return False, "Aprobador no existe."
    approver = approver_doc.to_dict()
    if approver.get("role") != "admin" or not approver.get("approved", False):
        return False, "Solo un administrador aprobado puede rechazar solicitudes."

    req_doc = db.collection("admin_approvals").document(token).get()
    if not req_doc.exists:
        return False, "Token inválido o inexistente."

    req = req_doc.to_dict()
    if req.get("status") != "pending":
        return False, "Esta solicitud ya fue procesada."

    # Actualizar solicitud
    db.collection("admin_approvals").document(token).update({
        "status": "rejected",
        "rejected_by": approver_username,
        "rejected_at": datetime.now(timezone.utc).isoformat()
    })

    # Opcional: notificar al usuario objetivo
    try:
        subject = "Avatars vs Rooks: solicitud de administrador rechazada"
        body = (
            f"Hola {req['target_username']},\n\n"
            f"Tu solicitud para acceder como administrador fue rechazada por {approver_username}."
        )
        send_email(req["target_email"], subject, body)
    except Exception:
        pass

    return True, "Solicitud rechazada."
