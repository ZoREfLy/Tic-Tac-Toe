from flask import Flask, jsonify, render_template, request

from game.session import GameSession

app = Flask(__name__)
session = GameSession()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/new-game", methods=["POST"])
def new_game():
    mode = request.json.get("mode")
    try:
        state = session.new_game(mode)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(state)


@app.route("/api/move", methods=["POST"])
def move():
    row = request.json.get("row")
    col = request.json.get("col")
    state = session.make_move(row, col)
    return jsonify(state)


@app.route("/api/train", methods=["POST"])
def train():
    stats = GameSession.train()
    return jsonify(stats)


@app.route("/api/model-exists")
def model_exists():
    return jsonify({"exists": GameSession.model_exists()})


if __name__ == "__main__":
    app.run(debug=True)
