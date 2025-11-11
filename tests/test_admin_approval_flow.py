"""
Test de integración: aprobación o rechazo de solicitudes de administrador.

Este test interactúa con Firestore REAL.
Permite aprobar o rechazar manualmente una solicitud pendiente
usando un token copiado desde la colección 'admin_approvals'.
"""


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.auth.admin_approval import approve_admin_by_token, reject_admin_by_token
from DBconfig.firebase_config import db

@pytest.mark.integration
def test_admin_approval_flow():
    print("\n=== Test de aprobación de administradores ===\n")

    # Listar solicitudes pendientes
    pending = list(db.collection("admin_approvals").where("status", "==", "pending").stream())

    if not pending:
        print("No hay solicitudes pendientes en Firestore.")
        return

    print(f"Se encontraron {len(pending)} solicitudes pendientes:\n")
    for doc in pending:
        data = doc.to_dict()
        print(f"- Token: {data['token']}")
        print(f"  Usuario: {data['target_username']}")
        print(f"  Correo: {data['target_email']}")
        print(f"  País: {data['nationality']['name'] if isinstance(data.get('nationality'), dict) else data.get('nationality')}")
        print(f"  Solicitado el: {data['requested_at']}\n")

    # Pedir token manualmente
    token = input("Ingrese el token que desea aprobar o rechazar: ").strip()
    action = input("¿Desea (A)probar o (R)echazar esta solicitud? ").strip().lower()
    approver = input("Ingrese su username de administrador aprobador: ").strip().lower()

    # Verificar existencia del token antes de ejecutar acción
    req_doc = db.collection("admin_approvals").document(token).get()
    if not req_doc.exists:
        print(" Token no encontrado.")
        return

    # Ejecutar acción
    if action == "a":
        ok, msg = approve_admin_by_token(token, approver)
    elif action == "r":
        ok, msg = reject_admin_by_token(token, approver)
    else:
        print("Acción no válida. Use 'A' o 'R'.")
        return

    print("\n--- RESULTADO ---")
    print(f"Estado: {'Éxito' if ok else 'Error'}")
    print(f"Mensaje: {msg}\n")

    # Verificar que el documento cambió de estado
    updated = db.collection("admin_approvals").document(token).get().to_dict()
    print(f"Nuevo estado en Firestore: {updated.get('status')}")
    print(f"Aprobado por: {updated.get('approved_by')}")
    print(f"Aprobado en: {updated.get('approved_at')}")
    print("\n==============================\n")
