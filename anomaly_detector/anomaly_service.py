from flask import Flask, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

app = Flask(__name__)

@app.route('/detect-anomalies', methods=['GET'])
def detect_anomalies():
    try:
        file_path = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Combined data file not found."}), 404

        df = pd.read_csv(file_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")

        # Select features with less missing data
        selected_features = ["SYSTEM_DEMAND", "CO2_INTENSITY", "WIND_ACTUAL"]

        # Drop rows with NaNs in selected features
        clean_df = df.dropna(subset=selected_features).copy()

        if clean_df.empty:
            return jsonify({"error": "No valid data in selected features. Cannot perform anomaly detection."}), 400

        # Fit the Isolation Forest on the clean data
        model = IsolationForest(contamination=0.01, random_state=42)
        clean_df["anomaly"] = model.fit_predict(clean_df[selected_features])
        clean_df["anomaly_label"] = clean_df["anomaly"].apply(lambda x: "anomaly" if x == -1 else "normal")

        # Merge results back into full df for full context
        df = df.merge(clean_df[["Timestamp", "anomaly_label"]], on="Timestamp", how="left")

        anomalies = df[df["anomaly_label"] == "anomaly"]
        # Save the updated DataFrame with anomaly labels
        
        df.to_csv(file_path, index=False)
        
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
