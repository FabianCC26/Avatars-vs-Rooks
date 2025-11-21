from DBconfig.firebase_config import db


def actualizar_best_score(user_id: str, new_score: int, database=db):


    doc_ref = database.collection("hall_of_fame").document(user_id)
    doc = doc_ref.get()

    # Si no existe el documento, crear registro inicial
    if not doc.exists:
        doc_ref.set({"best_score": new_score})
        return True

    data = doc.to_dict() or {}
    current_best = data.get("best_score", 0)

    # Solo actualizar si es mayor
    if new_score > current_best:
        doc_ref.update({"best_score": new_score})
        return True

    return False

def obtener_top_scores(database=db):
    """
    Devuelve lista ordenada de usuarios por best_score (DESC).
    """
    docs = database.collection("hall_of_fame").stream()
    resultados = []

    for d in docs:
        data = d.to_dict() or {}
        resultados.append({
            "user_id": d.id,
            "best_score": data.get("best_score", 0)
        })

    # Orden DESC (mayor a menor)
    resultados.sort(key=lambda x: x["best_score"], reverse=True)
    return resultados

