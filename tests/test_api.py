"""Tests d'intégration pour l'API FastAPI."""

from fastapi.testclient import TestClient
from src.api.app import app


def test_health_check_endpoint() -> None:
    """Vérifie que la route de monitoring renvoie un statut 200 et ok."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app_name"] == "retech-price-predictor"


def test_predict_endpoint_valid_payload() -> None:
    """Vérifie qu'une requête conforme produit un prix prédit cohérent."""
    payload = {
        "brand": "Dell",
        "processor": "Intel Core i5-1135G7",
        "ram_gb": 16,
        "storage_gb": 512,
        "screen_size_inch": 14.0,
        "condition": "Très bon état",
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_price_eur" in data
        assert data["predicted_price_eur"] > 0
        assert data["status"] == "success"


def test_predict_endpoint_invalid_payload() -> None:
    """Vérifie que Pydantic bloque les entrées hors limites (ex: RAM négative)."""
    invalid_payload = {
        "brand": "Dell",
        "processor": "Intel Core i5",
        "ram_gb": -4,
        "storage_gb": 512,
        "screen_size_inch": 14.0,
        "condition": "Bon état",
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 422
