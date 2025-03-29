from flask import Flask, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import os

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def forecast_demand():
    file_path = '/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv'
    try:
        # Load data
        df = pd.read_csv(file_path, parse_dates=['Timestamp'])

        # Ensure the Timestamp column is the DataFrame index
        df.set_index('Timestamp', inplace=True)

        # Aggregate demand (example: summing across regions)
        if 'SYSTEM_DEMAND' in df.columns:
            df_demand = df['SYSTEM_DEMAND'].resample('15min').sum().ffill()
        else:
            return jsonify({"error": "SYSTEM_DEMAND column missing."})

        # ARIMA model (simple example)
        model = ARIMA(df_demand, order=(1, 1, 1))
        model_fit = model.fit()

        # Forecasting the next 24 hours (96 intervals for 15 min each)
        forecast = model_fit.forecast(steps=96)

        # Prepare forecast data
        forecast_data = [{"Timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'), "Forecasted_Demand": val}
                         for ts, val in zip(pd.date_range(start=df_demand.index[-1], periods=96, freq='15min'), forecast)]

        return jsonify({"status": "Forecast generated successfully.", "forecast": forecast_data})

    except FileNotFoundError:
        return jsonify({"error": "Combined data file not found."})
    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/', methods=['GET'])
def root():
    return "Demand forecaster is running.", 200
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
