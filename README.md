# Tic-Tac-Toe with Reinforcement Learning

A Tic-Tac-Toe game featuring an AI opponent trained via temporal-difference (TD) learning. Play in the terminal or through a web UI.

## How the AI Learns to Play

### The Core Idea

The AI doesn't know the rules of Tic-Tac-Toe strategy. Instead, it plays thousands of games against itself and learns from experience — specifically, from **who wins at the end**.

Every board position gets a **value** — a number between 0 and 1 representing "how good is this position for me?"

- **1.0** = "I won from here"
- **0.0** = "I lost from here"
- **0.5** = "no idea yet" (the starting value for unseen positions)

These values are stored in a big lookup table mapping board states to their learned values.

### How a Single Game Works

Say the AI plays a game and makes moves that produce these board states:

```
State A → State B → State C → WIN (1.0)
```

After the game ends, the AI walks **backwards** through its moves and updates values:

1. **State C** (last move before winning): set to **1.0** — "this position led directly to a win"
2. **State B**: was 0.5, nudge it **toward** State C's value — "this position led to a good position"
3. **State A**: was 0.5, nudge it **toward** State B's updated value — "this position eventually led to winning"

This is **Temporal Difference (TD) learning** — each state learns from the state that came *after* it. The "knowledge" of winning flows backwards through the chain, one step at a time, over many games.

### The Parameters

#### Learning Rate (`LEARNING_RATE = 0.5`)

**How much to adjust a value in a single update.**

```
new_value = old_value + learning_rate * (target - old_value)
```

- **High (close to 1.0)**: jump aggressively toward new information. Learns fast but can be unstable — one lucky game might overwrite thousands of games' worth of learning.
- **Low (close to 0.0)**: barely budge. Very stable but takes forever to learn.
- **0.5**: split the difference — move halfway toward the new target each time.

#### Discount Factor (`DISCOUNT_FACTOR = 0.9`)

**How much to trust the future.**

Without discounting, every move in the chain gets equal credit for a win. But the move right before winning deserves *more* credit than a random opening move. The discount factor handles this:

```
State C → value = 1.0          (terminal, no discount)
State B → nudge toward 0.9 * 1.0 = 0.9
State A → nudge toward 0.9 * B's value
```

Each step back multiplies by 0.9 again, so early moves get weaker signals. This helps the AI learn that "this move *directly* blocks a win" is more valuable than "this opening move *eventually* contributed to winning 5 moves later."

- **1.0**: no discounting, all moves get equal credit
- **0.0**: only the very last move matters
- **0.9**: good middle ground — recent moves matter most, but early moves still get some credit

#### Epsilon / Exploit Rate (`EXPLOIT_RATE = 0.7`)

**How often to pick the "best known" move vs. a random move.**

This is the explore-vs-exploit tradeoff:

- **With probability 0.7 (epsilon)**: pick the move that leads to the highest-valued board state — **exploit** what you've learned
- **With probability 0.3 (1 - epsilon)**: pick a random legal move — **explore** positions you haven't tried

Why explore at all? If the AI only ever picks its "best" move, it might never discover a *better* strategy. Random moves force it to try new things.

During training, this value **decays** — early on, the AI explores a lot (epsilon starts low at 0.1); later, it mostly exploits (epsilon rises to 0.9). After training, `greedy=True` means always exploit (epsilon = 1.0 effectively).

#### Training Episodes (`TRAINING_EPISODES = 50000`)

**How many self-play games to run.** More games = more experience = better values in the lookup table. With symmetry-aware hashing, 50,000 is plenty because the AI recognizes that a corner opening is the same board regardless of *which* corner.

### Canonical Hashing (Symmetry-Aware State Lookup)

A tic-tac-toe board can be rotated and flipped. These 8 boards are all strategically identical — the best move is the same, just rotated:

```
 O |   |        |   | O      |   |        |   |
-----------  -----------  -----------  -----------
   |   |        |   |        |   |        |   |
-----------  -----------  -----------  -----------
   |   |        |   |        |   | O    O |   |
 (original)   (90° CW)     (180°)    (270° CW)

   |   | O      |   |        |   |      O |   |
-----------  -----------  -----------  -----------
   |   |        |   |        |   |        |   |
-----------  -----------  -----------  -----------
   |   |        |   | O    O |   |        |   |
 (flipped)    (flip+90)  (flip+180)  (flip+270)
```

Without canonical hashing, the AI treats these as **8 separate positions** — it has to learn each one independently. That's 8x the work.

`canonical_hash` takes any board, generates all 8 symmetric versions, and always returns the **same key** (the lexicographically smallest one) for all of them. So all 8 of those boards map to the same memory entry. When the AI learns "an O in the corner on an empty board is worth 0.8", that knowledge instantly applies to **all four corners** — no need to learn each one separately.

The impact:
- State space shrinks ~8x (fewer positions to learn)
- Training converges much faster (every game teaches 8x more)
- This is why `TRAINING_EPISODES` can be 50,000 instead of 200,000 and still get better results

### Putting It All Together

```
For 50,000 games:
    1. Play a full game (AI vs itself)
    2. At each turn, pick a move:
       - 70% chance: pick the move leading to highest-valued state (exploit)
       - 30% chance: pick a random move (explore)
    3. When game ends (win/loss/tie), walk backwards through moves:
       - Last state = result (1.0 / 0.0 / 0.5)
       - Each earlier state: nudge toward (discount * next state's value)
       - Nudge amount controlled by learning rate

After training:
    - The memory table has good values for thousands of positions
    - Always pick the highest-valued move (greedy)
    - Result: an AI that wins ~99% against random play
```

## Running

### Terminal

```bash
python3 cli.py
```

Select mode `0` for Human vs AI, `1` for Human vs Human. If no trained model exists, training runs automatically.

### Web UI

```bash
python3 -m web.app
```

### Dependencies

Python, NumPy, Flask (for web UI).

## Testing

```bash
python3 -m pytest tests/ -v
```
