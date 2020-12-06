from flask import Flask, render_template, request, jsonify
import json

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
        print(distribution)
        
        return 'Mot indice : 3'

    # GET request
    else:
        message = {'test':'Hello !'}
        return jsonify(message)

if __name__ == "__main__":
    app.run()
