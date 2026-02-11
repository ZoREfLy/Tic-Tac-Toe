from game.session import GameSession

KEY_MAP = {
    "Q": (0, 0), "W": (0, 1), "E": (0, 2),
    "A": (1, 0), "S": (1, 1), "D": (1, 2),
    "Z": (2, 0), "X": (2, 1), "C": (2, 2),
}

SYMBOLS = {1: " O ", -1: " X ", 0: "   "}


def format_board(board):
    """Convert a nested-list board to a text grid."""
    cells = [SYMBOLS[cell] for row in board for cell in row]
    return "{}|{}|{}\n-----------\n{}|{}|{}\n-----------\n{}|{}|{}\n".format(*cells)


def get_key_move():
    """Read a QWEASDZXC key and return (row, col)."""
    while True:
        move = input("Your move: ").upper()
        if move not in KEY_MAP:
            print("Invalid key! Use Q/W/E/A/S/D/Z/X/C.")
            continue
        return KEY_MAP[move]


def play():
    session = GameSession()

    while True:
        raw = input("0 for Human-AI, 1 for Human-Human: ")
        if raw == "0":
            mode = "human-ai"
            break
        elif raw == "1":
            mode = "human-human"
            break
        print("Invalid input! Enter 0 or 1.")

    print("Instruction:")
    print(" Q | W | E \n-----------\n A | S | D \n-----------\n Z | X | C \n")

    if mode == "human-ai" and not GameSession.model_exists():
        print("Training...")
        stats = GameSession.train()
        print(f"P1: {stats['p1_wins']}\nP2: {stats['p2_wins']}\nT: {stats['ties']}")

    state = session.new_game(mode)
    print(format_board(state["board"]))

    while not state["done"]:
        row, col = get_key_move()
        state = session.make_move(row, col)
        if "error" in state:
            print(state["error"])
            continue
        print(format_board(state["board"]))

    print("Game Over!")
    if not state["winner"]:
        print("Tie!")
    else:
        print(f"The winner is {state['winner']}!")


if __name__ == "__main__":
    play()
