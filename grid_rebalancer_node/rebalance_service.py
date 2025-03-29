from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Grid Rebalancer node is running."

@app.route("/rebalance", methods=["GET"])
def rebalance():
    try:
        file_path = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Combined data file not found."}), 404

        df = pd.read_csv(file_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")

        result = {}

        for region in ["ALL", "ROI", "NI"]:
            regional_data = df[df["Region"] == region]
            mean_demand = regional_data["SYSTEM_DEMAND"].mean()
            peak_demand = regional_data["SYSTEM_DEMAND"].max()
            deviation = abs(peak_demand - mean_demand)

            result[region] = {
                "mean_demand": round(mean_demand, 2),
                "peak_demand": round(peak_demand, 2),
                "demand_deviation": round(deviation, 2),
                "rebalancing_required": bool(deviation > 1000)  # <-- Convert to native bool
            }

        return jsonify({
            "status": "Rebalancing operation completed.",
            "rebalancing_summary": result,
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008)