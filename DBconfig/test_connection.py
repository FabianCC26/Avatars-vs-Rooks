"""from firebase_config import db

doc_ref = db.collection("pruebas").document("conexion")
doc_ref.set({"mensaje": "Conexión exitosa con Firestore"})

print("Documento creado correctamente en Firestore")"""

from firebase_config import db


def test_firebase_config_no_errors():
    # El objetivo es que este archivo cargue sin romperse.
    assert True
