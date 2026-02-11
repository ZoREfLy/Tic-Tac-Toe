import os
import tempfile

import numpy as np

from game.agent import Agent


def test_choose_action_returns_valid_move():
    agent = Agent(1)
    state = np.zeros((3, 3))
    i, j, symbol = agent.choose_action(state)
    assert 0 <= i <= 2
    assert 0 <= j <= 2
    assert symbol == 1
    assert state[i, j] == 0  # state restored after lookahead


def test_greedy_picks_best_value():
    agent = Agent(1)
    state = np.zeros((3, 3))

    # Pre-populate memory so (0,0) has the highest value
    state[0, 0] = 1
    agent.memory[state.tobytes()] = 1.0
    state[0, 0] = 0

    for i in range(3):
        for j in range(3):
            if (i, j) != (0, 0):
                state[i, j] = 1
                agent.memory[state.tobytes()] = 0.0
                state[i, j] = 0

    i, j, _ = agent.choose_action(state, greedy=True)
    assert (i, j) == (0, 0)


def test_train_updates_memory_values():
    agent = Agent(1)
    state = np.zeros((3, 3))

    state[0, 0] = 1
    h1 = state.tobytes()
    agent.memory[h1] = 0.5
    agent.moves.append(h1)

    state[1, 1] = 1
    h2 = state.tobytes()
    agent.memory[h2] = 0.5
    agent.moves.append(h2)

    agent.train(1.0)
    assert agent.memory[h2] == 1.0
    assert agent.memory[h1] != 0.5


def test_save_load_roundtrip():
    agent = Agent(1)
    state = np.zeros((3, 3))
    state[0, 0] = 1
    agent.memory[state.tobytes()] = 0.8

    with tempfile.NamedTemporaryFile(suffix=".dat", delete=False) as f:
        tmp_path = f.name

    try:
        agent.save(tmp_path)
        agent2 = Agent(1)
        agent2.load(tmp_path)
        assert agent2.memory == agent.memory
    finally:
        os.unlink(tmp_path)
