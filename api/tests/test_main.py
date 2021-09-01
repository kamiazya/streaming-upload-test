from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_upload():
    response = client.post("/", b"1234567890")
    assert response.status_code == 200
    assert response.json() == {
        "chunkSizes": [10],
        "totalSize": 10,
        "maxSize": 10,
        "minSize": 10,
    }
