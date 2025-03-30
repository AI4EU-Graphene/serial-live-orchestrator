from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

app = Flask(__name__)

FILE_PATH = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
SELECTED_FEATURES = ["SYSTEM_DEMAND", "CO2_INTENSITY", "WIND_ACTUAL"]

@app.route("/", methods=["GET"])
def root():
    return "Anomaly detector is running.", 200

@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "Anomaly Detector",
        "description": "Detects anomalies in energy metrics using Isolation Forest.",
        "input": ["Combined_Preprocessed_For_ML.csv"],  # 💥 match preprocessor output
        "output": ["anomaly_label"],
        "tags": ["anomaly", "ml", "energy"]
    })

@app.route("/detect-anomalies", methods=["GET"])
def detect_anomalies():
    try:
        if not os.path.exists(FILE_PATH):
            return jsonify({"error": "Combined data file not found."}), 404

        df = pd.read_csv(FILE_PATH)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")

        # If already labeled, return summary directly
        if "anomaly_label" in df.columns:
            anomalies = df[df["anomaly_label"] == "anomaly"]
            return jsonify({
                "status": "Anomaly labels already present.",
                "total_rows": len(df),
                "anomalies_found": len(anomalies),
                "anomaly_timestamps": anomalies["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()
            })

        # Filter valid rows for model training
        clean_df = df.dropna(subset=SELECTED_FEATURES).copy()
        if clean_df.empty:
            return jsonify({"error": "No valid data in selected features. Cannot perform anomaly detection."}), 400

        # Train Isolation Forest and label anomalies
        model = IsolationForest(contamination=0.01, random_state=42)
        clean_df["anomaly"] = model.fit_predict(clean_df[SELECTED_FEATURES])
        clean_df["anomaly_label"] = clean_df["anomaly"].apply(lambda x: "anomaly" if x == -1 else "normal")

        # Merge anomaly labels back into full dataset
        df = df.merge(clean_df[["Timestamp", "anomaly_label"]], on="Timestamp", how="left")

        # Save updated data
        df.to_csv(FILE_PATH, index=False)

        anomalies = df[df["anomaly_label"] == "anomaly"]
        return jsonify({
            "status": "Anomaly detection complete.",
            "total_rows": len(df),
            "anomalies_found": len(anomalies),
            "anomaly_timestamps": anomalies["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5006)