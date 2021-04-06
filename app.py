print("Launching ...")
from flask import Flask, render_template, request, jsonify
import json
from AI import AI_3
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
    # POST request
    if request.method == 'POST':
        
        json_msg = request.get_json()
        # distribution = json.loads(json_msg)
        distribution = json_msg['distribution']
        color = json_msg['color']
        # ai = json_msg['ai']
        print("------------ Called for color : ", getColorName(color))
        word_to_guess, enemy_words, neutral, assassin = getWords(distribution, color)
        
        # # ---------- TEST -----------
        # best_clue, best_score, best_g = "", "", ""
        start, finish = 0, 0
        allResults = "error"
        # try:
            # allResults = EmbeddingsAI.get_clue(word_to_guess, enemy_words, neutral, assassin)
        allResults = AI_manager(word_to_guess, enemy_words, neutral, assassin)
        # except :
        #     pass
        print("WAOZSHOWAUZHDOU : ", allResults)
        return json.dumps(allResults,  separators=(',', ':'))
        # return allResults
        

    # GET request
    else:
        message = {'test':'Hello !'}
        return jsonify(message)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8000))
    # app.run(host="0.0.0.0")
    app.run()

# -----------------------------------

