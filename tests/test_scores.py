import pytest
from unittest.mock import MagicMock
from src.ranks.hall_of_fame import actualizar_best_score, obtener_top_scores


def test_actualizar_best_score_menor():
    # Mock DB
    mock_db = MagicMock()

    # Simula un best_score actual de 90
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {"best_score": 90}

    mock_db.collection.return_value.document.return_value.get.return_value = mock_doc

    # Llamar la función con score menor (NO debe actualizar)
    result = actualizar_best_score("user123", 70, mock_db)

    assert result is False
    mock_db.collection.return_value.document.return_value.update.assert_not_called()


def test_top_scores_ordenados():
    # Mock DB
    mock_db = MagicMock()

    # Mock documents
    mock_doc_user1 = MagicMock()
    mock_doc_user1.id = "userA"
    mock_doc_user1.to_dict.return_value = {"best_score": 120}

    mock_doc_user2 = MagicMock()
    mock_doc_user2.id = "userB"
    mock_doc_user2.to_dict.return_value = {"best_score": 80}

    # Simular la colección hall_of_fame
    mock_db.collection.return_value.stream.return_value = [
        mock_doc_user1,
        mock_doc_user2
    ]

    # Llamar la función
    resultados = obtener_top_scores(mock_db)

    # Verificar orden (mayor → menor)
    assert resultados[0]["user_id"] == "userA"
    assert resultados[0]["best_score"] == 120

    assert resultados[1]["user_id"] == "userB"
    assert resultados[1]["best_score"] == 80

    # Verificar largo
    assert len(resultados) == 2