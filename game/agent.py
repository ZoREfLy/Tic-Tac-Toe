import random
import pickle

import numpy as np

from game.config import EXPLOIT_RATE, LEARNING_RATE


class Agent:
    """RL agent using temporal-difference learning."""

    def __init__(self, symbol, learning_rate=LEARNING_RATE, epsilon=EXPLOIT_RATE):
        self.moves = []
        self.memory = {}
        self.symbol = symbol
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    def reset(self):
        self.moves = []

    def choose_action(self, state, greedy=False):
        candidate_hashes = []
        candidate_values = []
        candidate_positions = []

        for i in range(3):
            for j in range(3):
                if state[i, j] == 0:
                    candidate_positions.append((i, j))
                    state[i, j] = self.symbol
                    hash_code = state.tobytes()
                    candidate_hashes.append(hash_code)
                    if hash_code not in self.memory:
                        self.memory[hash_code] = 0.5
                    candidate_values.append(self.memory[hash_code])
                    state[i, j] = 0

        if np.random.rand() < self.epsilon or greedy:
            best = max(candidate_values)
            indices = [i for i, v in enumerate(candidate_values) if v == best]
            index = random.choice(indices)
        else:
            index = random.randint(0, len(candidate_hashes) - 1)

        action = candidate_positions[index]
        self.remember(candidate_hashes[index])
        return action[0], action[1], self.symbol

    def remember(self, hash_code):
        self.moves.append(hash_code)

    def train(self, result):
        self.moves.reverse()
        self.memory[self.moves[0]] = next_value = result
        for h in self.moves[1:]:
            self.memory[h] += self.learning_rate * (next_value - self.memory[h])
            next_value = self.memory[h]
        self.reset()

    def save(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self.memory, f)

    def load(self, file_name):
        with open(file_name, "rb") as f:
            self.memory = pickle.load(f)
