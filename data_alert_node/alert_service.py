# alert_service.py
from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

THRESHOLD = 20  # Number of anomalies to trigger alert

@app.route('/check-alert', methods=['GET'])
def check_alert():
    try:
        file_path = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Combined data file not found."}), 404

        df = pd.read_csv(file_path)

        if "anomaly_label" not in df.columns:
            return jsonify({"error": "Anomaly labels not found. Run anomaly detection first."}), 400

        anomaly_count = (df["anomaly_label"] == "anomaly").sum()

        alert_status = "ALERT" if anomaly_count > THRESHOLD else "NORMAL"

        return jsonify({
            "status": alert_status,
            "anomalies_detected": int(anomaly_count),
            "threshold": int(THRESHOLD)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
