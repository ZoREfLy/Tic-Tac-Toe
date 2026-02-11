import numpy as np


class GameEngine:
    """Pure game state and rules — no I/O."""

    PLAYER_NAMES = {3: "Player 1", -3: "Player 2"}

    def __init__(self):
        self.state = np.zeros((3, 3))
        self.done = False
        self.winner = None

    def reset(self):
        self.state[:, :] = 0
        self.done = False
        self.winner = None

    def make_move(self, row, col, player):
        """Place *player* (1 or -1) at (row, col). Returns False if cell is occupied."""
        if self.state[row, col] != 0:
            return False
        self.state[row, col] = player
        self.check_winner()
        return True

    def get_valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.state[i, j] == 0]

    def check_winner(self):
        # Columns
        for col in range(3):
            total = sum(self.state[:, col])
            if total in self.PLAYER_NAMES:
                self.done = True
                self.winner = self.PLAYER_NAMES[total]
                return

        # Rows
        for row in range(3):
            total = sum(self.state[row, :])
            if total in self.PLAYER_NAMES:
                self.done = True
                self.winner = self.PLAYER_NAMES[total]
                return

        # Diagonal (top-left to bottom-right)
        total = sum(self.state[i, i] for i in range(3))
        if total in self.PLAYER_NAMES:
            self.done = True
            self.winner = self.PLAYER_NAMES[total]
            return

        # Diagonal (bottom-left to top-right)
        total = self.state[0, 2] + self.state[1, 1] + self.state[2, 0]
        if total in self.PLAYER_NAMES:
            self.done = True
            self.winner = self.PLAYER_NAMES[total]
            return

        # Tie
        if 0 not in self.state:
            self.done = True

    def state_to_display(self):
        cells = []
        for val in np.nditer(self.state):
            if val == -1:
                cells.append(" X ")
            elif val == 0:
                cells.append("   ")
            else:
                cells.append(" O ")
        return "{}|{}|{}\n-----------\n{}|{}|{}\n-----------\n{}|{}|{}\n".format(*cells)
