from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Define the node registry with full metadata config
NODE_REGISTRY = {
    "ml-preprocessor": {"host": "ml-preprocessor", "port": 5010, "meta": "/meta"},
    "ml-forecaster": {"host": "ml-forecaster", "port": 5011, "meta": "/meta"},
    "storage-optimizer": {"host": "storage-optimizer", "port": 5009, "meta": "/meta"},
    "anomaly-detector": {"host": "anomaly-detector", "port": 5006, "meta": "/meta"},
    "data-rebalancer": {"host": "data-rebalancer", "port": 5008, "meta": "/meta"},
    "context-service": {"host": "context-service", "port": 5012, "meta": "/meta"},
    "alert-node": {"host": "alert-node", "port": 5007, "meta": "/meta"},
    "data-source": {"host": "data-ingestor", "port": 5004, "meta": "/meta"}  # ✅ this is the fix
}

# Fallback metadata for virtual or static nodes
VIRTUAL_NODE_META = {
    "data-source": {
    "host": "data-ingestor",        # 🔥 this is the actual container name!
    "port": 5004,
    "meta": "/meta"
}
}

@app.route("/", methods=["GET"])
def root():
    return "Registry node is running."

@app.route("/list-nodes", methods=["GET"])
def list_nodes():
    return jsonify({"nodes": list(NODE_REGISTRY.keys())})

@app.route("/node-meta", methods=["GET"])
def get_node_meta():
    results = {}
    for name, config in NODE_REGISTRY.items():
        if config is None:
            # Virtual node, use static fallback
            results[name] = VIRTUAL_NODE_META.get(name, {"error": "No metadata available"})
        else:
            url = f"http://{config['host']}:{config['port']}{config['meta']}"
            try:
                res = requests.get(url)
                results[name] = res.json()
                results[name]["host"] = config["host"]
                results[name]["port"] = config["port"]
            except Exception as e:
                results[name] = {"error": str(e)}
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5014)