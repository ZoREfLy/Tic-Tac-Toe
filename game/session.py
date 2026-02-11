import os

from game.engine import GameEngine
from game.agent import Agent
from game.trainer import Trainer
from game.config import MODEL_DIR


class GameSession:
    """Frontend-agnostic game orchestration.

    Any UI (CLI, web, desktop) drives a game through this class.
    """

    MODES = ("human-ai", "human-human")

    def __init__(self):
        self._engine = GameEngine()
        self._mode = None
        self._current_player = 1
        self._ai = None

    def new_game(self, mode):
        """Start a new game. *mode* must be "human-ai" or "human-human"."""
        if mode not in self.MODES:
            raise ValueError(f"Invalid mode {mode!r}. Choose from {self.MODES}")
        self._mode = mode
        self._current_player = 1
        self._engine.reset()

        if mode == "human-ai":
            p2_path = os.path.join(MODEL_DIR, "p2.dat")
            if os.path.exists(p2_path):
                self._ai = Agent(-1)
                self._ai.load(p2_path)
            else:
                self._ai = None
        else:
            self._ai = None

        return self.get_state()

    def make_move(self, row, col):
        """Process a human move and, in human-ai mode, auto-play the AI response.

        Returns a state dict. On invalid moves the dict includes an ``error`` key.
        """
        if self._mode is None:
            return {**self.get_state(), "error": "No game in progress. Call new_game() first."}

        if self._engine.done:
            return {**self.get_state(), "error": "Game is already over."}

        if not self._engine.make_move(row, col, self._current_player):
            return {**self.get_state(), "error": "Cell already occupied."}

        self._current_player *= -1
        state = self.get_state()

        # AI auto-response in human-ai mode
        if self._mode == "human-ai" and self._ai and not self._engine.done:
            i, j, symbol = self._ai.choose_action(self._engine.state, greedy=True)
            self._engine.make_move(i, j, symbol)
            self._current_player *= -1
            state = self.get_state()
            state["ai_move"] = [i, j]

        return state

    def get_state(self):
        """Return the current game state as a JSON-serializable dict."""
        return {
            "board": self._engine.state.tolist(),
            "current_player": self._current_player,
            "done": self._engine.done,
            "winner": self._engine.winner,
            "mode": self._mode,
        }

    @staticmethod
    def train(progress_callback=None):
        """Run self-play training and save models. Returns stats dict."""
        engine = GameEngine()
        agent1 = Agent(1)
        agent2 = Agent(-1)
        trainer = Trainer(engine, agent1, agent2)
        stats = trainer.run(progress_callback)
        os.makedirs(MODEL_DIR, exist_ok=True)
        agent1.save(os.path.join(MODEL_DIR, "p1.dat"))
        agent2.save(os.path.join(MODEL_DIR, "p2.dat"))
        return stats

    @staticmethod
    def model_exists():
        """Check whether a trained model is available."""
        return os.path.exists(os.path.join(MODEL_DIR, "p2.dat"))
