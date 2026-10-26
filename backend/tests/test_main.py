import pytest
from fastapi.testclient import TestClient

from backend.main import MAX_MESSAGE_LENGTH, app

client = TestClient(app)

ERROR_DETAIL = f"Message must be between 1 and {MAX_MESSAGE_LENGTH} characters."
FRONTEND_ORIGIN = "http://127.0.0.1:5500"


def preflight(origin):
    return client.options(
        "/chat",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_reply_for_valid_message():
    response = client.post("/chat", json={"message": "What are your business hours?"})
    assert response.status_code == 200
    reply = response.json()["reply"]
    assert isinstance(reply, str) and reply != ""


def test_chat_trims_surrounding_spaces():
    response = client.post("/chat", json={"message": "  hello  "})
    assert response.status_code == 200
    assert response.json()["reply"].endswith("You said: hello")


def test_chat_accepts_message_of_exactly_max_length():
    response = client.post("/chat", json={"message": "a" * MAX_MESSAGE_LENGTH})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        {"message": ""},
        {"message": "   "},
        {"message": "a" * (MAX_MESSAGE_LENGTH + 1)},
        {},
        {"message": 123},
        {"message": None},
    ],
)
def test_chat_rejects_invalid_messages(body):
    response = client.post("/chat", json=body)
    assert response.status_code == 422
    assert response.json() == {"detail": ERROR_DETAIL}


def test_chat_rejects_malformed_json():
    response = client.post(
        "/chat", content="not json", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": ERROR_DETAIL}


def test_cors_allows_frontend_origin():
    response = preflight(FRONTEND_ORIGIN)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == FRONTEND_ORIGIN


def test_cors_blocks_unknown_origin():
    response = preflight("http://evil.example")
    assert "access-control-allow-origin" not in response.headers