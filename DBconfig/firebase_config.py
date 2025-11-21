import os

json_path = os.path.join("DBconfig", "avatar-vs-rooks-firebase-adminsdk-fbsvc-20a18344a3.json")

# Si el archivo NO existe → estamos en pytest o falta el archivo → NO iniciar Firebase
if not os.path.exists(json_path):
    db = None
else:
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
