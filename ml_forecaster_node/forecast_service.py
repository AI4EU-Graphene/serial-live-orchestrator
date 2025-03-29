from flask import Flask, jsonify
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "ML Forecaster node is running."

@app.route("/train-forecast", methods=["GET"])
def train_and_forecast():
    try:
        file_path = "/app/Downloaded_Data/Combined_Preprocessed_For_ML.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Preprocessed ML file not found."}), 404

        df = pd.read_csv(file_path)

        if "SYSTEM_DEMAND" not in df.columns:
            return jsonify({"error": "'SYSTEM_DEMAND' column not found in data."}), 400

        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp")

        # Convert timestamp to numerical features
        df["hour"] = df["Timestamp"].dt.hour
        df["dayofweek"] = df["Timestamp"].dt.dayofweek
        df["month"] = df["Timestamp"].dt.month

        features = [
            "CO2_EMISSIONS", "CO2_INTENSITY", "GEN_EXP", "SNSP_ALL", 
            "WIND_ACTUAL", "hour", "dayofweek", "month"
        ]
        df = df.dropna(subset=features + ["SYSTEM_DEMAND"])

        X = df[features]
        y = df["SYSTEM_DEMAND"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        joblib.dump(model, "/app/Downloaded_Data/random_forest_model.pkl")

        return jsonify({
            "status": "Forecast model trained successfully.",
            "rows_used": len(df),
            "mse_on_test": round(mse, 2),
            "model_path": "/app/Downloaded_Data/random_forest_model.pkl"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5011)