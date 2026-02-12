import random

import numpy as np

from game.agent import Agent, canonical_hash
from game.engine import GameEngine
from game.trainer import Trainer


def test_discount_factor_applied():
    agent = Agent(1, discount_factor=0.9)
    state = np.zeros((3, 3))

    # Simulate 3 moves
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

    s3 = s2.copy()
    s3[2, 2] = 1
    h3 = canonical_hash(s3)
    agent.memory[h3] = 0.5
    agent.moves.append(h3)

    agent.train(1.0)

    # Terminal state gets full reward
    assert agent.memory[h3] == 1.0
    # Discount means: terminal > middle > earliest
    assert agent.memory[h3] > agent.memory[h2] > agent.memory[h1]


def test_epsilon_decay():
    engine = GameEngine()
    agent1 = Agent(1)
    agent2 = Agent(-1)
    orig_eps = agent1.epsilon
    trainer = Trainer(engine, agent1, agent2, episodes=100)
    stats = trainer.run()

    # Original epsilon restored after training
    assert agent1.epsilon == orig_eps
    assert agent2.epsilon == orig_eps
    # Stats sum to total episodes
    assert stats["p1_wins"] + stats["p2_wins"] + stats["ties"] == 100


def test_state_not_mutated():
    agent = Agent(1)
    state = np.array([[1, -1, 0],
                      [0, 1, 0],
                      [-1, 0, 0]], dtype=float)
    original = state.copy()
    agent.choose_action(state)
    assert np.array_equal(state, original)


def test_symmetry_hash():
    state = np.zeros((3, 3))
    state[0, 0] = 1

    hashes = set()
    for k in range(4):
        rotated = np.rot90(state, k)
        hashes.add(canonical_hash(rotated))
        hashes.add(canonical_hash(np.fliplr(rotated)))

    assert len(hashes) == 1


def test_trained_ai_beats_random():
    engine = GameEngine()
    agent1 = Agent(1)
    agent2 = Agent(-1)
    trainer = Trainer(engine, agent1, agent2, episodes=5000)
    trainer.run()

    # Evaluate: trained agent1 (greedy) vs random opponent
    wins = 0
    for _ in range(100):
        engine.reset()
        first_player = True
        while not engine.done:
            if first_player:
                i, j, sym = agent1.choose_action(engine.state, greedy=True)
                engine.make_move(i, j, sym)
                agent1.reset()
            else:
                r, c = random.choice(engine.get_valid_moves())
                engine.make_move(r, c, -1)
            first_player = not first_player
        if engine.winner == "Player 1":
            wins += 1

    assert wins > 80
