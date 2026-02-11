from game.engine import GameEngine


def test_empty_board_no_winner():
    engine = GameEngine()
    assert not engine.done
    assert engine.winner is None


def test_row_win():
    engine = GameEngine()
    for j in range(3):
        engine.make_move(0, j, 1)
    assert engine.done
    assert engine.winner == "Player 1"


def test_col_win():
    engine = GameEngine()
    for i in range(3):
        engine.make_move(i, 0, -1)
    assert engine.done
    assert engine.winner == "Player 2"


def test_diagonal_win():
    engine = GameEngine()
    for i in range(3):
        engine.make_move(i, i, 1)
    assert engine.done
    assert engine.winner == "Player 1"


def test_tie_detection():
    engine = GameEngine()
    # O X O
    # O X X
    # X O O
    moves = [
        (0, 0, 1), (0, 1, -1), (0, 2, 1),
        (1, 0, 1), (1, 1, -1), (1, 2, -1),
        (2, 0, -1), (2, 1, 1), (2, 2, 1),
    ]
    for r, c, p in moves:
        engine.make_move(r, c, p)
    assert engine.done
    assert engine.winner is None


def test_invalid_move_returns_false():
    engine = GameEngine()
    engine.make_move(0, 0, 1)
    assert engine.make_move(0, 0, -1) is False


def test_make_move_alternates_player():
    engine = GameEngine()
    engine.make_move(0, 0, 1)
    engine.make_move(1, 1, -1)
    assert engine.state[0, 0] == 1
    assert engine.state[1, 1] == -1
