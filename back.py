from flask import Flask, render_template, request

app = Flask(__name__, template_folder="./static")

@app.route("/")
def test():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return "login test"

if __name__ == "__main__":
    app.run()
