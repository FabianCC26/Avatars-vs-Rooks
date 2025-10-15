from firebase_config import db

doc_ref = db.collection("pruebas").document("conexion")
doc_ref.set({"mensaje": "Conexión exitosa con Firestore"})

print("Documento creado correctamente en Firestore")
