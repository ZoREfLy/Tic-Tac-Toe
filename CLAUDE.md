# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python3 cli.py
```

The game prompts for mode selection: `0` for Human vs AI, `1` for Human vs Human. Dependencies: Python, NumPy.

## Testing

```bash
pytest tests/ -v
```

## Architecture

```
cli.py                  # Console entry point (thin I/O wrapper over GameSession)
game/
    __init__.py
    engine.py           # GameEngine — pure state & rules, no I/O
    agent.py            # Agent — RL agent (temporal difference learning)
    trainer.py          # Trainer — self-play training loop
    session.py          # GameSession — frontend-agnostic game orchestration
    config.py           # Hyperparameters & constants
web/
    __init__.py
    app.py              # Flask app — thin JSON wrapper over GameSession
    templates/
        index.html      # Single-page UI
    static/
        style.css       # CSS Grid board, responsive layout
        game.js         # fetch calls, board rendering, click handlers
tests/
    test_engine.py
    test_agent.py
    test_trainer.py
    test_session.py
    test_api.py
```

- **game/engine.py** — `GameEngine` class. Manages the 3x3 board state as a NumPy array. Pure game logic with no I/O: `reset()`, `make_move(row, col, player)`, `get_valid_moves()`, `check_winner()`, `state_to_display()`. Player 1 uses `1`, Player 2 uses `-1`, empty cells are `0`. Win detection checks if any row/col/diagonal sums to `3` or `-3`.

- **game/agent.py** — `Agent` class. RL agent using temporal difference learning. Stores state values in a hash table (`state.tobytes()` → float). During training, explores with probability `1 - epsilon` (random move) and exploits with probability `epsilon` (greedy). Trained models are saved/loaded as `.dat` files via pickle.

- **game/trainer.py** — `Trainer` class. Runs self-play training between two agents. Constructor takes engine, two agents, episode count. `run()` returns stats dict `{p1_wins, p2_wins, ties}`. Accepts optional progress callback.

- **game/session.py** — `GameSession` class. Frontend-agnostic game orchestration — the single entry point any UI uses to drive a game. Methods: `new_game(mode)` starts a game (`"human-ai"` or `"human-human"`), `make_move(row, col)` processes a move (auto-includes AI response in human-ai mode), `get_state()` returns a JSON-serializable dict `{board, current_player, done, winner, mode}`. Static helpers: `train()` runs self-play training, `model_exists()` checks for a saved model.

- **game/config.py** — Constants: `TRAINING_EPISODES`, `LEARNING_RATE`, `EXPLOIT_RATE`, `MODEL_DIR`.

- **cli.py** — Thin console I/O wrapper over `GameSession`. Keyboard input maps QWEASDZXC to the 3x3 grid positions. In Human-AI mode, if no trained model exists, training runs automatically before the game starts.

- **web/app.py** — Flask app. Thin JSON wrapper over `GameSession` with 5 routes: `GET /` (serves HTML), `POST /api/new-game`, `POST /api/move`, `POST /api/train`, `GET /api/model-exists`. Run with `python3 -m web.app`.
