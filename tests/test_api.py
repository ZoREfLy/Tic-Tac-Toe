import os

import pytest

from web.app import app
from game.config import MODEL_DIR


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_html(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.content_type


def test_new_game_returns_empty_board(client):
    res = client.post("/api/new-game", json={"mode": "human-human"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["board"] == [[0, 0, 0]] * 3
    assert data["done"] is False


def test_move_updates_state(client):
    client.post("/api/new-game", json={"mode": "human-human"})
    res = client.post("/api/move", json={"row": 0, "col": 0})
    data = res.get_json()
    assert data["board"][0][0] == 1
    assert "error" not in data


def test_ai_responds_after_human_move(client):
    if not os.path.exists(os.path.join(MODEL_DIR, "p2.dat")):
        pytest.skip("No trained model available")
    client.post("/api/new-game", json={"mode": "human-ai"})
    res = client.post("/api/move", json={"row": 0, "col": 0})
    data = res.get_json()
    if not data["done"]:
        assert "ai_move" in data


def test_invalid_move_returns_error(client):
    client.post("/api/new-game", json={"mode": "human-human"})
    client.post("/api/move", json={"row": 0, "col": 0})
    res = client.post("/api/move", json={"row": 0, "col": 0})
    data = res.get_json()
    assert "error" in data


def test_game_over_detection(client):
    client.post("/api/new-game", json={"mode": "human-human"})
    # Player 1 wins across row 0
    client.post("/api/move", json={"row": 0, "col": 0})  # P1
    client.post("/api/move", json={"row": 1, "col": 0})  # P2
    client.post("/api/move", json={"row": 0, "col": 1})  # P1
    client.post("/api/move", json={"row": 1, "col": 1})  # P2
    res = client.post("/api/move", json={"row": 0, "col": 2})  # P1 wins
    data = res.get_json()
    assert data["done"] is True
    assert data["winner"] == "Player 1"
