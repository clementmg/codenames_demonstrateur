print("Launching ...")
from flask import Flask, render_template, request, jsonify
import json
from AI import AI_3
from AI import EmbeddingsAI
import time
from utils import getWords

app = Flask(__name__, template_folder="./static")

@app.route("/")
@app.route('/ai3', methods=['GET', 'POST'])
def callAi():
    # POST request
    if request.method == 'POST' or request.method == "GET":
        
        json_msg = request.get_json()
        # distribution = json.loads(json_msg)
        distribution = json_msg['distribution']
        color = json_msg['color']
        print("COLOR IS : ", color)
        word_to_guess, enemy_words, neutral, assassin = getWords(distribution, color)
        
        # # ---------- TEST -----------
        # best_clue, best_score, best_g = "", "", ""
        start, finish = 0, 0
        allResults = "error"
        try:
            start = time.time()
            allResults = EmbeddingsAI.get_clue(word_to_guess, enemy_words, neutral, assassin)
            finish = time.time()
        except :
            pass
        
        elapsed_time = finish - start
        
        return json.dumps([allResults, round(elapsed_time, 2)],  separators=(',', ':'))
        # return allResults
        

    # GET request
    # else:
    #     message = {'test':'Hello !'}
    #     return jsonify(message)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8000))
    # app.run(host="0.0.0.0")
    app.run()

# -----------------------------------

