let currentMode = null;
let gameDone = false;

const cells = document.querySelectorAll(".cell");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game-btn");
const trainBtn = document.getElementById("train-btn");

cells.forEach(cell => {
    cell.addEventListener("click", () => {
        if (gameDone) return;
        if (cell.classList.contains("disabled")) return;
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        makeMove(row, col);
    });
});

async function newGame(mode) {
    currentMode = mode;
    const res = await fetch("/api/new-game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mode})
    });
    if (!res.ok) {
        const data = await res.json();
        statusEl.textContent = data.error || "Error starting game";
        return;
    }
    const state = await res.json();
    renderBoard(state);
    newGameBtn.style.display = "inline-block";
    trainBtn.style.display = "none";
}

async function makeMove(row, col) {
    const res = await fetch("/api/move", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({row, col})
    });
    const state = await res.json();
    if (state.error) {
        statusEl.textContent = state.error;
        return;
    }
    renderBoard(state);
    if (state.ai_move) {
        const [ar, ac] = state.ai_move;
        const aiCell = document.querySelector(`.cell[data-row="${ar}"][data-col="${ac}"]`);
        if (aiCell) {
            aiCell.classList.add("ai-move");
            setTimeout(() => aiCell.classList.remove("ai-move"), 500);
        }
    }
}

function renderBoard(state) {
    const symbols = {1: "O", "-1": "X", 0: ""};
    gameDone = state.done;

    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);
        const val = state.board[r][c];
        cell.textContent = symbols[val] || "";
        cell.className = "cell";
        if (val === 1) cell.classList.add("cell-o");
        else if (val === -1) cell.classList.add("cell-x");
        if (gameDone || val !== 0) cell.classList.add("disabled");
    });

    if (state.done) {
        if (state.winner === 1) statusEl.textContent = "Player O wins!";
        else if (state.winner === -1) statusEl.textContent = "Player X wins!";
        else statusEl.textContent = "It's a tie!";
    } else {
        const player = state.current_player === 1 ? "O" : "X";
        statusEl.textContent = `Player ${player}'s turn`;
    }
}

async function trainModel() {
    statusEl.textContent = "Training AI model... please wait.";
    trainBtn.disabled = true;
    const res = await fetch("/api/train", {method: "POST"});
    const stats = await res.json();
    statusEl.textContent = `Training done! P1: ${stats.p1_wins}, P2: ${stats.p2_wins}, Ties: ${stats.ties}`;
    trainBtn.style.display = "none";
}

async function checkModel() {
    const res = await fetch("/api/model-exists");
    const data = await res.json();
    if (!data.exists) {
        statusEl.textContent = "No trained model found. Train first to play vs AI.";
        trainBtn.style.display = "inline-block";
    }
}

checkModel();
