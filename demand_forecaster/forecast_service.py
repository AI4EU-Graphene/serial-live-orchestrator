from flask import Flask, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

app = Flask(__name__)
DATA_PATH = "/app/Downloaded_Data/Combined_Preprocessed_For_ML.csv"
MODEL_PATH = "/app/Downloaded_Data/random_forest_model.pkl"

@app.route("/", methods=["GET"])
def root():
    return "Demand Forecaster is running.", 200

@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({
        "name": "Demand Forecaster",
        "description": "Uses ARIMA or Random Forest to forecast energy demand based on historical patterns.",
        "input": ["Combined_Preprocessed_For_ML.csv"],
        "output": ["Forecasted_Demand"],
        "tags": ["forecast", "ml", "energy"]
    })

@app.route("/train-forecast", methods=["GET"])
def train_forecast():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "Preprocessed data file not found."}), 404

        df = pd.read_csv(DATA_PATH)
        df.dropna(subset=["SYSTEM_DEMAND"], inplace=True)

        X = df.index.values.reshape(-1, 1)
        y = df["SYSTEM_DEMAND"].values

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)

        return jsonify({
            "status": "Forecast model trained successfully.",
            "model_path": MODEL_PATH,
            "rows_used": len(df),
            "mse_on_test": 0.0  # Placeholder
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5011)