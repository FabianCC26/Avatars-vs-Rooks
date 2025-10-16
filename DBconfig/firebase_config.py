import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("DBconfig/avatar-vs-rooks-firebase-adminsdk-fbsvc-20a18344a3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
