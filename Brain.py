import random
import numpy as np

class Brain:
	"""
	This object remembers each state and its probability to result
	"""
	def __init__(self, symbol, learning_rate=0.5, epsilon=0.7):
		self.moves = []
		self.memory = {}
		self.symbol = symbol
		self.epsilon = epsilon
		self.learning_rate = learning_rate

	def reset(self):
		del self.moves
		self.moves = []

	def choose_action(self, state, full=None):
		candidate_states_hashs = []
		candidate_states_values = []
		candidate_states_positions = []

		# find all possible moves
		for i in range(0, 3):
			for j in range(0, 3):
				if state[i, j] == 0:
					candidate_states_positions.append((i, j)) # remember the position of the possible move
					state[i, j] = self.symbol # temporarily change the state
					
					hash_codes = state.tobytes() # calculate the hash code of the temporary state
					candidate_states_hashs.append(hash_codes) # remember the hash code

					# if the temporary state is not in memory, save it and set the value to default (0.5)
					if hash_codes not in self.memory:
						self.memory[hash_codes] = 0.5
					candidate_states_values.append(self.memory[hash_codes]) # remember the value of the temporary state

					state[i, j] = 0 # change back to original state
		
		if np.random.rand() < self.epsilon or full: # choose an action according to action values

			# remember all actions that have max value
			indices = [i for i, v in enumerate(candidate_states_values) if v == max(candidate_states_values)]
			
			if len(indices) == 1: # only one action has the highest value
				index = indices[0]
				action = candidate_states_positions[index]
				self.remember(candidate_states_hashs[index])
				return action[0], action[1], self.symbol
			else: # multiple actions have the highest value
				index = random.choice(indices) # randomly choose one of them
				action = candidate_states_positions[index]
				self.remember(candidate_states_hashs[index])
				return action[0], action[1], self.symbol
		else: # randomly choose an action by avoiding local minima
			index = random.randint(0, len(candidate_states_hashs)-1)
			action = candidate_states_positions[index]
			self.remember(candidate_states_hashs[index])
			return action[0], action[1], self.symbol

	def remember(self, hash_code):
		self.moves.append(hash_code)

	def train(self, result):
		self.moves.reverse()
		self.memory[self.moves[0]] = next_state_value = result

		for i in self.moves[1:]:
			self.memory[i] += self.learning_rate * (next_state_value - self.memory[i])
			next_state_value = self.memory[i]

		self.reset()
		# print(self.memory)

	def save(self, file_name):
		with open(file_name, 'w') as f:
			for key, val in self.memory.items():
				f.write('{} {}\n'.format(key, val))

	def load(self, file_name):
		with open(file_name, 'r') as f:
			for line in f:
				key, val = line.split()
				self.memory[key] = val
		