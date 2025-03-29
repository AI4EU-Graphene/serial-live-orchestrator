from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def optimize_load():
    try:
        data = request.get_json()
        forecast = data.get("forecast", [])

        if not forecast:
            return jsonify({"error": "No forecast data provided"}), 400

        optimized_forecast = []
        total_original = 0
        total_optimized = 0

        for day in forecast:
            original = day["predicted_demand_MW"]
            optimized = round(original * 0.92, 2)  # Simulate a 8% efficiency gain
            optimized_forecast.append({
                "date": day["date"],
                "original_demand_MW": original,
                "optimized_demand_MW": optimized
            })
            total_original += original
            total_optimized += optimized

        peak_reduction = round(100 * (1 - (total_optimized / total_original)), 2)

        return jsonify({
            "optimization": optimized_forecast,
            "efficiency_gain_percent": peak_reduction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/', methods=['GET'])
def root():
    return "Load optimizer is running.", 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
