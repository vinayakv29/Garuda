from flask import Flask, request, jsonify, render_template
from filter import GarudaFilter

# starting the flask app
app = Flask(__name__)

# one instance of the filter is enough
checker = GarudaFilter()

@app.route("/")
def home():
    return render_template("index.html")

# this route receives a message and returns analysis
@app.route("/check", methods=["POST"])
def check_message():
    incoming = request.get_json()
    msg = incoming.get("message", "")
    result = checker.analyze(msg)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
