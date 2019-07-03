import os
import numpy as np

from Brain import Brain


class Board:
	"""
	This object allows player(s) to take actions,
	remembers the current state of game, remembers
	and prints the current state of game
	"""
	def __init__(self):
		self.done = False
		self.winner = None
		self.first_player = True
		self.state = np.zeros((3, 3))
		self.player = {3: 'Player 1', -3: 'Player 2'}
		self.operations = {'Q': (0, 0), 'W': (0, 1), 'E': (0, 2),
						'A': (1, 0), 'S': (1, 1), 'D': (1, 2),
						'Z': (2, 0), 'X': (2, 1), 'C': (2, 2)}

	def is_done(self):
		# detect if there are 3 same symbols in the same column
		for col in range(0, 3):
			total = sum(self.state[:, col])
			if total == 3 or total == -3:
				self.done = True
				self.winner = self.player[total]
				return

		# detect if there are 3 same symbols in the same row
		for row in range(0, 3):
			total = sum(self.state[row, :])
			if total == 3 or total == -3:
				self.done = True
				self.winner = self.player[total]
				return

		# detect if there are 3 same symbols in diagonal (up-left to bottom-right)
		total = 0
		for i in range(0, 3):
			total += self.state[i, i]
		if total == 3 or total == -3:
			self.done = True
			self.winner = self.player[total]
			return

		# detect if there are 3 same symbols in diagonal (bottom-left to up-right)
		total = self.state[0, 2] + self.state[1, 1] + self.state[2, 0]
		if total == 3 or total == -3:
			self.done = True
			self.winner = self.player[total]
			return

		if 0 not in self.state:
			self.done = True

	def reset(self):
		self.done = False
		self.winner = None
		self.state[:, :] = 0
		self.first_player = True

	def step(self, i, j, player=None):
		if not player:
			if self.first_player:
				self.state[i, j] = 1
			else:
				self.state[i, j] = -1
		else:
			self.state[i, j] = player

		self.is_done()

	def __str__(self):
		row = []
		for i in np.nditer(self.state):
			if i == -1:
				row += [' X ']
			elif i == 0:
				row += ['   ']
			else:
				row += [' O ']
		return '{}|{}|{}\n-----------\n{}|{}|{}\n-----------\n{}|{}|{}\n'.format(*row)

	def train(self):
		print('Training...')
		p1 = p2 = t = 0
		self.AI_1 = Brain(1)
		self.AI_2 = Brain(-1)

		for _ in range(9000):
			self.reset()
			# print(self)

			while not self.done:
				if self.first_player:
					player = self.AI_1
				else:
					player = self.AI_2

				i, j, symbol = player.choose_action(self.state)
				self.step(i, j, symbol)

				# print(self)

				self.first_player = not self.first_player

			# self.game_over()

			if self.winner == 'Player 1':
				p1 += 1
				self.AI_1.train(1)
				self.AI_2.train(0)
			elif self.winner == 'Player 2':
				p2 += 1
				self.AI_1.train(0)
				self.AI_2.train(1)
			else:
				t += 1
				self.AI_1.train(0.5)
				self.AI_2.train(0.5)

		print('P1: {}\nP2: {}\nT: {}'.format(p1, p2, t))
		self.AI_1.save('p1.dat')
		self.AI_2.save('p2.dat')

	def play(self):
		self.reset()
		mode = int(input("0 for Human-AI, 1 for Human-Human: "))

		if mode in range(2):
				print("Instruction:")
				print(' Q | W | E \n-----------\n A | S | D \n-----------\n Z | X | C \n')
				print(self)

				if mode == 0:
					if os.path.exists('p2.dat'):
						self.AI_2 = Brain(-1)
						self.AI_2.load('p2.dat')
					else:
						self.train()
						self.reset()

					while not self.done:
						if self.first_player:
							move = input("Your move: ")
							self.step(*self.operations[move.upper()])
							self.first_player = not self.first_player
							print(self)
						else:
							i, j, symbol = self.AI_2.choose_action(self.state, True)
							self.step(i, j, symbol)
							self.first_player = not self.first_player
							print(self)
				else:
					while not self.done:
						move = input("Your move: ")

						self.step(*self.operations[move.upper()])

						self.first_player = not self.first_player

						print(self)
						# print(self.state)

				self.game_over()

	def game_over(self):
		print("Game Over!")
		if not self.winner:
			print("Tire!")
		else:
			print("The winner is {}!".format(self.winner))

if __name__ == '__main__':
	board = Board()
	# board.train()
	board.play()
