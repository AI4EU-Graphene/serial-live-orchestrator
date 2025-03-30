from flask import Flask, jsonify
import requests
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)
REGISTRY_URL = "http://registry-node:5014/node-meta"

NODE_ACTION_ENDPOINTS = {
    "Data Source": "/get-demand",
    "ML Preprocessor": "/ml-preprocess",
    "Demand Forecaster": "/train-forecast",
    "Storage Optimizer": "/optimize-storage",
    "Anomaly Detector": "/detect-anomalies",
    "Grid Rebalancer": "/rebalance"
}

@app.route("/", methods=["GET"])
def root():
    return "Smart Agent node is running.", 200

@app.route("/smart-run", methods=["GET"])
def smart_run():
    try:
        registry = requests.get(REGISTRY_URL).json()
        energy_nodes = {
            name: meta for name, meta in registry.items()
            if isinstance(meta, dict) and "tags" in meta and "energy" in meta["tags"]
        }

        output_to_node = {}
        for node, meta in energy_nodes.items():
            for output in meta.get("output", []):
                output_to_node[output] = node

        sorted_nodes, visited = [], set()

        while len(sorted_nodes) < len(energy_nodes):
            progress = False
            for node, meta in energy_nodes.items():
                if node in visited:
                    continue
                inputs = meta.get("input", [])
                unsatisfied = [
                    inp for inp in inputs if inp in output_to_node and output_to_node[inp] not in visited
                ]
                if not unsatisfied:
                    sorted_nodes.append(node)
                    visited.add(node)
                    progress = True
            if not progress:
                return jsonify({"error": "Cyclic dependency or unsortable pipeline."}), 500

        results = {}
        for node in sorted_nodes:
            meta = energy_nodes[node]
            host, port = meta["host"], meta["port"]
            action_endpoint = NODE_ACTION_ENDPOINTS.get(meta["name"])
            if not action_endpoint:
                results[meta["name"]] = {"error": f"No action endpoint defined for {meta['name']}"}
                continue

            url = f"http://{host}:{port}{action_endpoint}"
            try:
                res = requests.get(url, timeout=30)
                results[meta["name"]] = res.json()
            except Exception as e:
                results[meta["name"]] = {"error": str(e)}

        return jsonify({
            "status": "Smart workflow executed for context: energy",
            "pipeline": [energy_nodes[n]["name"] for n in sorted_nodes],
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5013)