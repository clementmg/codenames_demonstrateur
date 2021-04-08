print("Launching ...")
from flask import Flask, render_template, request, jsonify
import json
from AI import EmbeddingsAI
import time
from utils import getWords, getColorName
from AI.AI_manager import AI_manager

app = Flask(__name__, template_folder="./static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/ai3', methods=['GET', 'POST'])
def callAi():
    if request.method == 'POST':

        json_msg = request.get_json()
        distribution = json_msg['distribution']
        color = json_msg['color']
        ai = json_msg['ai']
        print("------------ Called for color : ", getColorName(color))
        word_to_guess, enemy_words, neutral, assassin = getWords(distribution, color)

        # # ---------- TEST -----------
        allResults = "error"
        allResults = AI_manager(ai, word_to_guess, enemy_words, neutral, assassin)
        print("================= Information sent =================")
        print(allResults[0])
        return json.dumps(allResults[0],  separators=(',', ':'))

    # default get request
    else:
        message = {'nothing to see'}
        return jsonify(message)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8000))
    # app.run(host="0.0.0.0")
    app.run()

# -----------------------------------

