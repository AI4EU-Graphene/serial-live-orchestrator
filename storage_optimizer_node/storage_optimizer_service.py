from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Storage Optimizer node is running."

@app.route("/optimize-storage", methods=["GET"])
def optimize_storage():
    try:
        file_path = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Combined data file not found."}), 404

        df = pd.read_csv(file_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        latest = df.sort_values("Timestamp").iloc[-1]

        demand = latest.get("SYSTEM_DEMAND", 0)
        generation = latest.get("GEN_EXP", 0)

        action = "idle"
        if generation - demand > 500:
            action = "charge"
        elif demand - generation > 500:
            action = "discharge"

        return jsonify({
            "status": "Storage optimization decision complete.",
            "latest_timestamp": latest["Timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            "demand": round(demand, 2),
            "generation": round(generation, 2),
            "action": action
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5009)