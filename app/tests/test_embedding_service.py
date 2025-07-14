import numpy as np
from app.services import embedding_service

GENRE_VECS = {
    "SF": np.array([1.0, 2.0, 3.0], dtype=np.float32),
    "Drama": np.array([4.0, 5.0, 6.0], dtype=np.float32),
    "Comedy": np.array([7.0, 8.0, 9.0], dtype=np.float32),
}

def fake_get_vector(name):
    return GENRE_VECS.get(name)

def test_calc_by_genre_mean(monkeypatch):
    from app.models import word2vec_util
    monkeypatch.setattr(word2vec_util, "get_vector", fake_get_vector)

    expected_mean = np.mean(list(GENRE_VECS.values()), axis=0)

    result = embedding_service.calc_by_genre(["SF", "Drama", "Comedy"])

    assert np.allclose(result, expected_mean)
    assert result.dtype == expected_mean.dtype
    assert result.shape == expected_mean.shape