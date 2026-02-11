import random

from game.config import TRAINING_EPISODES


class Trainer:
    """Runs self-play training between two agents.

    Uses a training schedule: early episodes favour exploration and random
    opponents so the agents discover all board positions; later episodes
    shift to exploitation and self-play to refine values.
    """

    def __init__(self, engine, agent1, agent2, episodes=TRAINING_EPISODES):
        self.engine = engine
        self.agent1 = agent1
        self.agent2 = agent2
        self.episodes = episodes

    def run(self, progress_callback=None):
        p1_wins = p2_wins = ties = 0
        orig_eps1 = self.agent1.epsilon
        orig_eps2 = self.agent2.epsilon
        orig_lr1 = self.agent1.learning_rate
        orig_lr2 = self.agent2.learning_rate

        for episode in range(self.episodes):
            self.engine.reset()
            progress = episode / self.episodes

            # Schedule: explore broadly early, exploit later
            self.agent1.epsilon = 0.1 + 0.8 * progress
            self.agent2.epsilon = 0.1 + 0.8 * progress
            self.agent1.learning_rate = orig_lr1 * (1 - 0.9 * progress)
            self.agent2.learning_rate = orig_lr2 * (1 - 0.9 * progress)

            # More random opponents early to cover all openings
            use_random_p1 = random.random() < (1 - progress) * 0.5

            first_player = True
            while not self.engine.done:
                if first_player:
                    if use_random_p1:
                        r, c = random.choice(self.engine.get_valid_moves())
                        self.engine.make_move(r, c, self.agent1.symbol)
                    else:
                        i, j, sym = self.agent1.choose_action(self.engine.state)
                        self.engine.make_move(i, j, sym)
                else:
                    i, j, sym = self.agent2.choose_action(self.engine.state)
                    self.engine.make_move(i, j, sym)
                first_player = not first_player

            if self.engine.winner == "Player 1":
                p1_wins += 1
                if not use_random_p1:
                    self.agent1.train(1)
                self.agent2.train(0)
            elif self.engine.winner == "Player 2":
                p2_wins += 1
                if not use_random_p1:
                    self.agent1.train(0)
                self.agent2.train(1)
            else:
                ties += 1
                if not use_random_p1:
                    self.agent1.train(0.5)
                self.agent2.train(0.5)

            if progress_callback:
                progress_callback(episode + 1, self.episodes)

        # Restore original hyperparameters
        self.agent1.epsilon = orig_eps1
        self.agent2.epsilon = orig_eps2
        self.agent1.learning_rate = orig_lr1
        self.agent2.learning_rate = orig_lr2

        return {"p1_wins": p1_wins, "p2_wins": p2_wins, "ties": ties}
