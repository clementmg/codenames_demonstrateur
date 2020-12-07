from flask import Flask, render_template, request, jsonify
import json
import AI_3
import time
from utils import getWords

app = Flask(__name__, template_folder="./static")

@app.route("/")
def test():
    return render_template("index.html")

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        
        json_msg = request.get_json()
        # distribution = json.loads(json_msg)
        distribution = json_msg['distribution']
        color = json_msg['color']
        print("COLOR IS : ", color)
        word_to_guess, enemy_words, neutral, assassin = getWords(distribution, color)
        
        # # ---------- TEST -----------
        start = time.time()
        best_clue, best_score, best_g = AI_3.get_clue(word_to_guess, enemy_words, neutral, assassin)
        finish = time.time()
        # best_clue = "test"
        return best_clue

    # GET request
    else:
        message = {'test':'Hello !'}
        return jsonify(message)

if __name__ == "__main__":
    app.run()

# -----------------------------------

