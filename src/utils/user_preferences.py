from DBconfig.firebase_config import db

def load_user_preferences(username: str) -> dict:
    """Obtiene las preferencias guardadas del usuario desde Firestore."""
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("preferences", {"theme": "light", "color": (0, 0, 0)})
    return {"theme": "light", "color": (0, 0, 0)}

def save_user_preferences(username: str, preferences: dict):
    """Guarda las preferencias del usuario en Firestore."""
    doc_ref = db.collection("users").document(username)
    doc_ref.update({"preferences": preferences})
