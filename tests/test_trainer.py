from game.engine import GameEngine
from game.agent import Agent
from game.trainer import Trainer


def test_training_runs_without_error():
    engine = GameEngine()
    agent1 = Agent(1)
    agent2 = Agent(-1)
    trainer = Trainer(engine, agent1, agent2, episodes=10)
    stats = trainer.run()
    assert isinstance(stats, dict)


def test_training_returns_stats():
    engine = GameEngine()
    agent1 = Agent(1)
    agent2 = Agent(-1)
    trainer = Trainer(engine, agent1, agent2, episodes=100)
    stats = trainer.run()
    assert "p1_wins" in stats
    assert "p2_wins" in stats
    assert "ties" in stats
    assert stats["p1_wins"] + stats["p2_wins"] + stats["ties"] == 100
