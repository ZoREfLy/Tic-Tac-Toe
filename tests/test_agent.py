import os
import tempfile

import numpy as np

from game.agent import Agent, canonical_hash


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

    # Pre-populate memory so corner (0,0) has the highest value
    candidate = state.copy()
    candidate[0, 0] = 1
    agent.memory[canonical_hash(candidate)] = 1.0

    for i in range(3):
        for j in range(3):
            if (i, j) != (0, 0):
                candidate = state.copy()
                candidate[i, j] = 1
                agent.memory[canonical_hash(candidate)] = 0.0

    i, j, _ = agent.choose_action(state, greedy=True)
    # All corners are symmetric under canonical_hash, so any corner is valid
    assert (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]


def test_train_updates_memory_values():
    agent = Agent(1)
    state = np.zeros((3, 3))

    s1 = state.copy()
    s1[0, 0] = 1
    h1 = canonical_hash(s1)
    agent.memory[h1] = 0.5
    agent.moves.append(h1)

    s2 = s1.copy()
    s2[1, 1] = 1
    h2 = canonical_hash(s2)
    agent.memory[h2] = 0.5
    agent.moves.append(h2)

    agent.train(1.0)
    assert agent.memory[h2] == 1.0
    assert agent.memory[h1] != 0.5


def test_save_load_roundtrip():
    agent = Agent(1)
    state = np.zeros((3, 3))
    state[0, 0] = 1
    agent.memory[canonical_hash(state)] = 0.8

    with tempfile.NamedTemporaryFile(suffix=".dat", delete=False) as f:
        tmp_path = f.name

    try:
        agent.save(tmp_path)
        agent2 = Agent(1)
        agent2.load(tmp_path)
        assert agent2.memory == agent.memory
    finally:
        os.unlink(tmp_path)
