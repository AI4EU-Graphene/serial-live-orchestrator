from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_PATH = "/app/Downloaded_Data/Combined_Preprocessed_For_ML.csv"

@app.route("/", methods=["GET"])
def root():
    return "Storage Optimizer is running.", 200

@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "Storage Optimizer",
        "description": "Decides whether to charge, discharge, or idle storage based on real-time supply-demand.",
        "input": ["Combined_Preprocessed_For_ML.csv"],
        "output": ["action"],
        "tags": ["energy", "storage", "optimizer"]
    })

@app.route("/optimize-storage", methods=["GET"])
def optimize_storage():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "Preprocessed data file not found."}), 404

        df = pd.read_csv(DATA_PATH)
        latest_row = df.iloc[-1]

        demand = latest_row["SYSTEM_DEMAND"]
        generation = latest_row["GEN_EXP"]

        action = "charge" if generation > demand else "discharge" if generation < demand else "idle"

        return jsonify({
            "status": "Storage optimization decision complete.",
            "latest_timestamp": latest_row["Timestamp"],
            "action": action,
            "demand": demand,
            "generation": generation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5009)