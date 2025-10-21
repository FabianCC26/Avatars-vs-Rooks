import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("DBconfig/avatar-vs-rooks-firebase-adminsdk-fbsvc-20a18344a3.json")
firebase_admin.initialize_app(cred)
API_KEY = "AIzaSyB0vNKFTx8_3PYNU0VAb7CXCvhMlfN6PYg" 
db = firestore.client()
