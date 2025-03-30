from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_PATH = "/app/Downloaded_Data/Combined_Preprocessed_For_ML.csv"

@app.route("/", methods=["GET"])
def root():
    return "Grid Rebalancer is running.", 200

@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "Grid Rebalancer",
        "description": "Analyzes regional demand to check if grid rebalancing is needed.",
        "input": ["Combined_Preprocessed_For_ML.csv"],
        "output": ["rebalancing_required"],
        "tags": ["energy", "grid", "rebalancer"]
    })

@app.route("/rebalance", methods=["GET"])
def rebalance():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "Preprocessed data file not found."}), 404

        df = pd.read_csv(DATA_PATH)
        summary = df.groupby("Region")["SYSTEM_DEMAND"].agg(["mean", "max", "std"]).to_dict()

        rebalancing_required = {}
        for region, metrics in summary["mean"].items():
            deviation = summary["std"][region]
            mean_demand = metrics
            peak_demand = summary["max"][region]
            rebalancing_required[region] = {
                "rebalancing_required": deviation > (0.5 * mean_demand),
                "demand_deviation": round(deviation, 2),
                "mean_demand": round(mean_demand, 2),
                "peak_demand": round(peak_demand, 2)
            }

        return jsonify({
            "status": "Rebalancing operation completed.",
            "rebalancing_summary": rebalancing_required,
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5008)