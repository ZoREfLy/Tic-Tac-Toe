import os

from game.engine import GameEngine
from game.agent import Agent
from game.trainer import Trainer
from game.config import MODEL_DIR

KEY_MAP = {
    "Q": (0, 0), "W": (0, 1), "E": (0, 2),
    "A": (1, 0), "S": (1, 1), "D": (1, 2),
    "Z": (2, 0), "X": (2, 1), "C": (2, 2),
}


def get_human_move(engine):
    while True:
        move = input("Your move: ").upper()
        if move not in KEY_MAP:
            print("Invalid key! Use Q/W/E/A/S/D/Z/X/C.")
            continue
        i, j = KEY_MAP[move]
        if engine.state[i, j] != 0:
            print("Cell already occupied! Choose another.")
            continue
        return i, j


def train_agents():
    print("Training...")
    engine = GameEngine()
    agent1 = Agent(1)
    agent2 = Agent(-1)
    trainer = Trainer(engine, agent1, agent2)
    stats = trainer.run()
    print(f"P1: {stats['p1_wins']}\nP2: {stats['p2_wins']}\nT: {stats['ties']}")
    os.makedirs(MODEL_DIR, exist_ok=True)
    agent1.save(os.path.join(MODEL_DIR, "p1.dat"))
    agent2.save(os.path.join(MODEL_DIR, "p2.dat"))
    return agent2


def play():
    engine = GameEngine()
    mode = int(input("0 for Human-AI, 1 for Human-Human: "))

    if mode not in (0, 1):
        return

    print("Instruction:")
    print(" Q | W | E \n-----------\n A | S | D \n-----------\n Z | X | C \n")
    print(engine.state_to_display())

    if mode == 0:
        p2_path = os.path.join(MODEL_DIR, "p2.dat")
        if os.path.exists(p2_path):
            ai = Agent(-1)
            ai.load(p2_path)
        else:
            ai = train_agents()
            engine.reset()
            print(engine.state_to_display())

        first_player = True
        while not engine.done:
            if first_player:
                i, j = get_human_move(engine)
                engine.make_move(i, j, 1)
            else:
                i, j, symbol = ai.choose_action(engine.state, greedy=True)
                engine.make_move(i, j, symbol)
            first_player = not first_player
            print(engine.state_to_display())
    else:
        first_player = True
        while not engine.done:
            i, j = get_human_move(engine)
            player = 1 if first_player else -1
            engine.make_move(i, j, player)
            first_player = not first_player
            print(engine.state_to_display())

    print("Game Over!")
    if not engine.winner:
        print("Tie!")
    else:
        print(f"The winner is {engine.winner}!")


if __name__ == "__main__":
    play()
