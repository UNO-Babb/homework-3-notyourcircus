from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

SAVE_FILE = "game_state.txt"

# Default game state
default_state = {
    "balance": 0,
    "status": "playing"
}


def load_game():
    """Load the saved game state from file, or return defaults."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return default_state
    return default_state


def save_game(state):
    """Save game state to file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)


@app.route("/")
def index():
    state = load_game()
    return render_template("index.html", state=state)


@app.route("/update_balance", methods=["POST"])
def update_balance():
    data = request.get_json()
    direction = data.get("direction")

    state = load_game()

    # Move balance based on key pressed
    if direction == "left":
        state["balance"] -= 1
    elif direction == "right":
        state["balance"] += 1

    # Check losing condition
    if state["balance"] <= -10 or state["balance"] >= 10:
        state["status"] = "fell"
    else:
        state["status"] = "playing"

    save_game(state)
    return jsonify(state)


@app.route("/reset", methods=["POST"])
def reset():
    save_game(default_state)
    return jsonify(default_state)


if __name__ == "__main__":
    app.run(debug=True)
