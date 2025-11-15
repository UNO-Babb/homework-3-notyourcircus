from flask import Flask, render_template, jsonify

app = Flask(__name__)
balance_angle = 0.0 
WOBBLE_STRENGTH = 2.0 

# Keep track of the current player
current_player = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/balance", methods=["POST"])
def balance():
    global balance_angle 

    data = request.get_json()
    player_input = data.get("input", 0)
     
    if player_input == "left":
        balance_angle -= 2
    elif player_input == "right":
        balance_angle += 2 
    balance_angle += random.uniform(-WOBBLE_STRENGTH, WOBBLE_STRENGTH)

    if abs(balance_angle) >= 45:
        return jsonify({ 
            "angle": balance_angle,
            "status": "fallen" 
        }) 
    
if __name__ == "__main__":
    app.run(debug=True)
