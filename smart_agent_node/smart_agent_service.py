from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Smart Agent node is running."

@app.route("/smart-run", methods=["GET"])
def smart_run():
    try:
        # Step 1: Get current deployment context
        context_response = requests.get("http://host.docker.internal:5012/context")
        context = context_response.json().get("context", "unknown")

        if context == "energy":
            steps = [
                ("ML Preprocessing", "http://ml-preprocessor:5010/ml-preprocess"),
                ("Model Training", "http://ml-forecaster:5011/train-forecast"),
                ("Storage Optimization", "http://storage-optimizer:5009/optimize-storage"),
                ("Anomaly Detection", "http://anomaly-detector:5006/detect-anomalies"),
                ("Alert Check", "http://alert-node:5007/check-alert"),
                ("Rebalance Grid", "http://data-rebalancer:5008/rebalance")
            ]
        else:
            return jsonify({"error": f"No pipeline configured for context: {context}"}), 400

        results = {}
        for name, url in steps:
            res = requests.get(url)
            results[name] = res.json()

        return jsonify({
            "status": "Smart workflow executed",
            "context": context,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5013)