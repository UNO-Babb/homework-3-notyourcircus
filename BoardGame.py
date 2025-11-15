from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

SAVE_FILE = "game_state.txt"

# Starting game state
game_state = {
    "balance": 0,      # 0 is centered; positive = right lean, negative = left lean
    "player": "Player 1",
    "status": "playing"
}

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data
    return game_state

def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

@app.route("/")
def index():
    current_state = load_game()
    return render_template("index.html", state=current_state)

@app.route("/update_balance", methods=["POST"])
def update_balance():
    data = request.get_json()
    direction = data.get("direction")

    state = load_game()

    if direction == "left":
        state["balance"] -= 1
    elif direction == "right":
        state["balance"] += 1

    # Lose condition: too far in either direction
    if state["balance"] <= -10 or state["balance"] >= 10:
        state["status"] = "fell"
    else:
        state["status"] = "playing"

    save_game(state)
    return jsonify(state)

@app.route("/reset", methods=["POST"])
def reset():
    global game_state
    game_state = {"balance": 0, "player": "Player 1", "status": "playing"}
    save_game(game_state)
    return jsonify(game_state)

if __name__ == "__main__":
    app.run(debug=True)
