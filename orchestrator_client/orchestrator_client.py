import json
import requests

def run_pipeline(input_number):
    # Load the blueprint (for legacy support, still square → cube)
    with open("orchestrator_client/blueprint.json") as f:
        blueprint = json.load(f)

    # Load grid profile to check enabled nodes
    with open("grid_profile.json") as f:
        grid_profile = json.load(f)

    enabled_nodes = grid_profile.get("enabled_nodes", [])

    # Optional: Demand Forecasting Node
    if "demand_forecaster" in enabled_nodes:
        print("\n📈 Demand Forecasting Node Triggered")
        try:
            forecast_response = requests.post("http://localhost:5002/forecast", json={"days": 5})
            forecast_data = forecast_response.json()
            for day in forecast_data["forecast"]:
                print(f"  {day['date']}: {day['predicted_demand_MW']} MW")
        except Exception as e:
            print(f"  ❌ Forecasting failed: {e}")

    # Optional: Load Optimization Node
    if "load_optimizer" in enabled_nodes:
        print("\n⚙️ Load Optimizer Node Triggered")
        try:
            optimize_response = requests.post("http://localhost:5003/optimize",
                                              json={"forecast": forecast_data["forecast"]})
            optimization_data = optimize_response.json()

            for entry in optimization_data["optimization"]:
                print(f"  {entry['date']}: {entry['optimized_demand_MW']} MW (from {entry['original_demand_MW']} MW)")

            print(f"  ⚡ Efficiency Gain: {optimization_data['efficiency_gain_percent']}%")

        except Exception as e:
            print(f"  ❌ Optimization failed: {e}")

    # Square Node
    print("\n🟧 Square Node Triggered")
    square_response = requests.post("http://localhost:5000/square", json={"number": input_number})
    square_output = square_response.json()["output"]
    print(f"  ✔️ Square Output: {square_output}")

    # Cube Node
    print("\n🟦 Cube Node Triggered")
    cube_response = requests.post("http://localhost:5001/cube", json={"number": square_output})
    cube_output = cube_response.json()["output"]
    print(f"  ✔️ Cube Output: {cube_output}")
if __name__ == "__main__":
    input_number = int(input("Enter a number to run through the pipeline: "))
    run_pipeline(input_number)