# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python Board.py
```

The game prompts for mode selection: `0` for Human vs AI, `1` for Human vs Human. No build step or dependencies beyond Python and NumPy.

## Architecture

This is a two-file Python Tic-Tac-Toe game with a reinforcement learning AI opponent.

- **Board.py** — Game engine and entry point. Manages the 3x3 board state as a NumPy array, handles player input, win/draw detection, and orchestrates training and gameplay. Player 1 uses `1`, Player 2 uses `-1`, empty cells are `0`. Win detection checks if any row/col/diagonal sums to `3` or `-3`. Keyboard input maps QWEASDZXC to the 3x3 grid positions.

- **Brain.py** — RL agent using temporal difference learning. Stores state values in a hash table (`state.tobytes()` → float). During training, explores with probability `1 - epsilon` (random move) and exploits with probability `epsilon` (greedy). After each game, backpropagates the result through visited states using the learning rate. Trained models are saved/loaded as `.dat` files (gitignored).

Training runs 9,000 self-play episodes between two Brain instances, then saves `p1.dat` and `p2.dat`. In Human-AI mode, if `p2.dat` doesn't exist, training runs automatically before the game starts.
