from flask import Flask, jsonify, request

app = Flask(__name__)
current_context = {"context": "unknown"}

@app.route("/", methods=["GET"])
def root():
    return "Context Service is running."

@app.route("/context", methods=["GET"])
def get_context():
    return jsonify(current_context)

@app.route("/set-context", methods=["POST"])
def set_context():
    data = request.get_json()
    new_context = data.get("context", "unknown")
    current_context["context"] = new_context
    return jsonify({"status": "Context updated", "context": new_context})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5012)