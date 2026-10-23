from fastapi.testclient import TestClient

from app.main import app


def test_frontend_cors_preflight():
    client = TestClient(app)

    response = client.options(
        "/api/trips/plan",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
