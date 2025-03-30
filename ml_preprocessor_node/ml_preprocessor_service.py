from flask import Flask, jsonify
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "ML Preprocessor node is running."

@app.route("/ml-preprocess", methods=["GET"])
def preprocess_for_ml():
    try:
        input_file = "/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv"
        output_file = "/app/Downloaded_Data/Combined_Preprocessed_For_ML.csv"

        if not os.path.exists(input_file):
            return jsonify({"error": "Input file not found."}), 404

        df = pd.read_csv(input_file)

        # Drop rows with NaNs in key features (you can customize these)
        features_to_use = [
            "CO2_EMISSIONS", "CO2_INTENSITY", "GEN_EXP",
            "INTER_NET", "SNSP_ALL", "SYSTEM_DEMAND", "WIND_ACTUAL"
        ]

        df = df.dropna(subset=features_to_use)

        # Extract only the selected features
        X = df[features_to_use]

        # Scale the data
        scaler = StandardScaler()
        scaled_X = scaler.fit_transform(X)

        # Create a new DataFrame with the same column names
        scaled_df = pd.DataFrame(scaled_X, columns=features_to_use)
        scaled_df["Timestamp"] = df["Timestamp"].values
        scaled_df["Region"] = df["Region"].values

        # Save to CSV
        scaled_df.to_csv(output_file, index=False)

        return jsonify({
            "status": "Preprocessing complete.",
            "rows_processed": len(scaled_df),
            "output_file": output_file
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "ML Preprocessor",
        "description": "Cleans and prepares data for machine learning.",
        "host": "ml-preprocessor",
        "port": 5010,
        "input": [
            "SYSTEM_DEMAND",
            "GEN_EXP",
            "CO2_INTENSITY",
            "WIND_ACTUAL",
            "Timestamp",
            "Region"
        ],
        "output": [
            "Cleaned_Data"
        ],
        "tags": ["preprocess", "ml", "energy"]
    })
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5010)