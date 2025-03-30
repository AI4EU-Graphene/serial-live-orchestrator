from flask import Flask, jsonify, request

app = Flask(__name__)

context_state = {"context": "energy"}  # default context

@app.route("/", methods=["GET"])
def root():
    return "Context Service is running.", 200

@app.route("/context", methods=["GET"])
def get_context():
    return jsonify(context_state)

@app.route("/set-context", methods=["POST"])
def set_context():
    try:
        data = request.get_json()
        context = data.get("context", None)
        if not context:
            return jsonify({"error": "No context provided"}), 400

        context_state["context"] = context
        return jsonify({"status": "Context updated", "context": context})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "Context Service",
        "description": "Manages global context state (e.g. energy, healthcare).",
        "input": [],
        "output": ["context"],
        "tags": ["context", "state", "global"]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5012)