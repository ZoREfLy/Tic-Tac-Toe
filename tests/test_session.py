import json
import os

import pytest

from game.session import GameSession
from game.config import MODEL_DIR


def test_new_game_human_human():
    session = GameSession()
    state = session.new_game("human-human")
    assert state["board"] == [[0, 0, 0]] * 3
    assert state["current_player"] == 1
    assert state["done"] is False
    assert state["winner"] is None
    assert state["mode"] == "human-human"


def test_new_game_invalid_mode_raises():
    session = GameSession()
    with pytest.raises(ValueError):
        session.new_game("invalid")


def test_make_move_basic():
    session = GameSession()
    session.new_game("human-human")
    state = session.make_move(0, 0)
    assert state["board"][0][0] == 1
    assert state["current_player"] == -1
    assert "error" not in state


def test_make_move_occupied_cell():
    session = GameSession()
    session.new_game("human-human")
    session.make_move(0, 0)
    state = session.make_move(0, 0)
    assert "error" in state
    assert "occupied" in state["error"].lower()


def test_make_move_after_game_over():
    session = GameSession()
    session.new_game("human-human")
    # Player 1 wins across row 0
    session.make_move(0, 0)  # P1
    session.make_move(1, 0)  # P2
    session.make_move(0, 1)  # P1
    session.make_move(1, 1)  # P2
    state = session.make_move(0, 2)  # P1 wins
    assert state["done"] is True
    # Trying another move after game over
    state = session.make_move(2, 2)
    assert "error" in state
    assert "over" in state["error"].lower()


def test_turn_alternation():
    session = GameSession()
    session.new_game("human-human")
    state = session.make_move(0, 0)
    assert state["board"][0][0] == 1  # P1
    state = session.make_move(1, 1)
    assert state["board"][1][1] == -1  # P2
    state = session.make_move(2, 2)
    assert state["board"][2][2] == 1  # P1 again


def test_tie_detection():
    session = GameSession()
    session.new_game("human-human")
    #  O | X | O        P1=1 at (0,0),(0,2),(1,0),(2,1),(2,2)
    #  O | X | X        P2=-1 at (0,1),(1,1),(1,2),(2,0)
    # X | O | O
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 1), (1, 0), (1, 2),
        (2, 1), (2, 0), (2, 2),
    ]
    for r, c in moves:
        state = session.make_move(r, c)
    assert state["done"] is True
    assert state["winner"] is None


def test_get_state_is_serializable():
    session = GameSession()
    session.new_game("human-human")
    session.make_move(0, 0)
    state = session.get_state()
    # Should not raise
    serialized = json.dumps(state)
    assert isinstance(serialized, str)


def test_human_ai_mode_ai_responds():
    if not os.path.exists(os.path.join(MODEL_DIR, "p2.dat")):
        pytest.skip("No trained model available")
    session = GameSession()
    session.new_game("human-ai")
    state = session.make_move(0, 0)
    if not state["done"]:
        # AI should have responded
        assert "ai_move" in state
        assert state["current_player"] == 1  # back to human's turn


def test_new_game_resets_state():
    session = GameSession()
    session.new_game("human-human")
    session.make_move(0, 0)
    session.make_move(1, 1)
    # Start a fresh game
    state = session.new_game("human-human")
    assert state["board"] == [[0, 0, 0]] * 3
    assert state["current_player"] == 1
    assert state["done"] is False
