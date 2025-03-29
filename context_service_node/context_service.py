from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Context service is running."

@app.route("/context", methods=["GET"])
def get_context():
    context_info = {
        "deployment_environment": "energy_grid",
        "enabled_nodes": [
            "data-ingestor",
            "data-preprocessor",
            "ml-preprocessor",
            "ml-forecaster",
            "demand-forecaster",
            "storage-optimizer",
            "grid-rebalancer",
            "anomaly-detector",
            "alert-node"
        ]
    }
    return jsonify(context_info)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5012)