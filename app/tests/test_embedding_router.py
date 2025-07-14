import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.services import embedding_service

client = TestClient(app)

def test_embedding_by_genre_returns_string_vector(monkeypatch):
    def fake_calc_by_genre(genres):
        return np.array([1.0, 2.0], dtype=np.float32)

    monkeypatch.setattr(embedding_service, "calc_by_genre", fake_calc_by_genre)

    payload = {"genres": ["SF", "Drama"]}
    resp = client.post("/embedding-by-genre", json=payload)

    assert resp.status_code == 200

    data = resp.json()
    assert data["vector"] == "[1.0, 2.0]"
