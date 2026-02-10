import os
import tempfile
import numpy as np
from unittest.mock import patch
from io import StringIO

from Brain import Brain
from Board import Board


def test_save_load_roundtrip():
    """Save a trained Brain, load into a new Brain, verify memory matches."""
    brain = Brain(1)
    # Simulate some learned states
    state = np.zeros((3, 3))
    state[0, 0] = 1
    key1 = state.tobytes()
    brain.memory[key1] = 0.8

    state[1, 1] = -1
    key2 = state.tobytes()
    brain.memory[key2] = 0.3

    with tempfile.NamedTemporaryFile(suffix='.dat', delete=False) as f:
        tmp_path = f.name

    try:
        brain.save(tmp_path)

        brain2 = Brain(1)
        brain2.load(tmp_path)

        assert brain2.memory == brain.memory
        # Verify values are floats, not strings
        for val in brain2.memory.values():
            assert isinstance(val, float)
        # Verify keys are bytes, not strings
        for key in brain2.memory.keys():
            assert isinstance(key, bytes)
    finally:
        os.unlink(tmp_path)


def test_invalid_input_handled():
    """Simulate invalid key input, confirm no crash and re-prompt."""
    board = Board()
    # Feed: invalid key 'P', then valid key 'Q'
    with patch('builtins.input', side_effect=['P', 'Q']):
        i, j = board.get_human_move()
    assert (i, j) == (0, 0)


def test_occupied_cell_rejected():
    """Attempt move on occupied cell, confirm rejected and re-prompt."""
    board = Board()
    board.state[0, 0] = 1  # Occupy the cell mapped to 'Q'
    # Feed: 'Q' (occupied), then 'W' (empty)
    with patch('builtins.input', side_effect=['Q', 'W']):
        i, j = board.get_human_move()
    assert (i, j) == (0, 1)


def test_tie_message(capsys):
    """Trigger a tie and verify output says 'Tie!' not 'Tire!'."""
    board = Board()
    board.done = True
    board.winner = None
    board.game_over()
    captured = capsys.readouterr()
    assert "Tie!" in captured.out
    assert "Tire!" not in captured.out
