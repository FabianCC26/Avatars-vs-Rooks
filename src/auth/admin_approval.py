# Módulo de aprobación de cuentas de administrador
# - Crea solicitudes de aprobación
# - Envía correos a administradores existentes
# - Permite aprobar por token desde el cliente (panel admin) o herramienta interna

import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List
from DBconfig.firebase_config import db
from src.utils.email_service import send_email  # Se asume que existe una función send_email(to, subject, body)
from google.cloud.firestore_v1 import DELETE_FIELD


def _admin_email_list() -> List[str]:
    """
    Obtiene la lista de correos de administradores aprobados.
    """
    emails: List[str] = []
    admins = db.collection("users").where("role", "==", "admin").where("approved", "==", True).stream()
    for doc in admins:
        data = doc.to_dict() or {}
        email = data.get("email")
        if isinstance(email, str) and email:
            emails.append(email)
    return emails


def create_admin_approval_request(target_username: str, target_email: str, target_display: str, nationality: Dict[str, Any]):
    """
    Crea un documento de solicitud de aprobación en 'admin_approvals' y notifica a los administradores.
    """
    token = secrets.token_urlsafe(32)
    req_ref = db.collection("admin_approvals").document(token)

    payload: Dict[str, Any] = {
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
    country_name = nationality.get("name") if isinstance(nationality, dict) else str(nationality)
    body = (
        f"Se solicitó acceso de administrador.\n\n"
        f"Usuario: {target_username}\n"
        f"Nombre: {target_display}\n"
        f"Nacionalidad: {country_name}\n"
        f"Correo: {target_email}\n\n"
        f"Token de aprobación: {token}\n"
        f"Instrucciones: Ingrese al panel de administradores del juego y apruebe esta solicitud usando el token.\n"
    )
    for to in to_list:
        try:
            send_email(to, subject, body)
        except Exception:
            # Evitar que un fallo de envío interrumpa el flujo
            pass


def approve_admin_by_token(token: str, approver_username: str) -> tuple[bool, str]:
    """
    Aprueba una solicitud por token. Debe llamarse desde un flujo donde 'approver_username'
    es un administrador aprobado. Devuelve (ok, mensaje).
    """
    approver_doc = db.collection("users").document(approver_username.lower()).get()
    if not approver_doc.exists:
        return False, "Aprobador no existe."

    approver = approver_doc.to_dict() or {}
    if approver.get("role") != "admin" or not approver.get("approved", False):
        return False, "Solo un administrador aprobado puede aprobar solicitudes."

    req_doc = db.collection("admin_approvals").document(token).get()
    if not req_doc.exists:
        return False, "Token inválido o inexistente."

    req = req_doc.to_dict() or {}
    if req.get("status") != "pending":
        return False, "Esta solicitud ya fue procesada."

    target_username = req.get("target_username")
    if not isinstance(target_username, str) or not target_username:
        return False, "Datos de la solicitud incompletos."

    user_ref = db.collection("users").document(target_username)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return False, "Usuario objetivo no existe."

    # Aprobar: marcar usuario como admin aprobado y eliminar el campo 'pending_admin_since'
    user_ref.update({
        "role": "admin",
        "approved": True,
        "approved_by": approver_username,
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "pending_admin_since": DELETE_FIELD
    })

    # Marcar solicitud como aprobada
    db.collection("admin_approvals").document(token).update({
        "status": "approved",
        "approved_by": approver_username,
        "approved_at": datetime.now(timezone.utc).isoformat()
    })

    # Avisar al usuario objetivo por correo
    try:
        target_email = req.get("target_email", "")
        if isinstance(target_email, str) and target_email:
            subject = "Avatars vs Rooks: solicitud de administrador aprobada"
            body = (
                f"Hola {target_username},\n\n"
                f"Tu solicitud para acceder como administrador ha sido aprobada por {approver_username}.\n"
                f"Ya puedes iniciar sesión con privilegios de administrador."
            )
            send_email(target_email, subject, body)
    except Exception:
        pass

    return True, "Solicitud aprobada correctamente."


def reject_admin_by_token(token: str, approver_username: str) -> tuple[bool, str]:
    """
    Rechaza una solicitud por token.
    """
    approver_doc = db.collection("users").document(approver_username.lower()).get()
    if not approver_doc.exists:
        return False, "Aprobador no existe."

    approver = approver_doc.to_dict() or {}
    if approver.get("role") != "admin" or not approver.get("approved", False):
        return False, "Solo un administrador aprobado puede rechazar solicitudes."

    req_doc = db.collection("admin_approvals").document(token).get()
    if not req_doc.exists:
        return False, "Token inválido o inexistente."

    req = req_doc.to_dict() or {}
    if req.get("status") != "pending":
        return False, "Esta solicitud ya fue procesada."

    # Actualizar solicitud como rechazada
    db.collection("admin_approvals").document(token).update({
        "status": "rejected",
        "rejected_by": approver_username,
        "rejected_at": datetime.now(timezone.utc).isoformat()
    })

    # Notificar al usuario objetivo
    try:
        target_username = req.get("target_username", "")
        target_email = req.get("target_email", "")
        if isinstance(target_email, str) and target_email:
            subject = "Avatars vs Rooks: solicitud de administrador rechazada"
            body = (
                f"Hola {target_username},\n\n"
                f"Tu solicitud para acceder como administrador fue rechazada por {approver_username}."
            )
            send_email(target_email, subject, body)
    except Exception:
        pass

    return True, "Solicitud rechazada."
