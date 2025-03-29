from flask import Flask, jsonify, request
import os
from datetime import datetime, timedelta
import asyncio
from EirGrid_Data_Download import async_eirgrid_downloader as edd

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "Data Ingestor node is running."

@app.route("/get-demand", methods=["GET"])
def get_demand():
    try:
        refresh = request.args.get("refresh", "false").lower() == "true"
        data_path = "/app/Downloaded_Data/ALL/ALL_demandactual_24_Eirgrid.csv"

        if not refresh:
            if os.path.exists(data_path):
                # Check if data is recent (e.g., less than 1 day old)
                modified_time = datetime.fromtimestamp(os.path.getmtime(data_path))
                if datetime.now() - modified_time < timedelta(days=1):
                    return jsonify({
                        "status": "Data already exists and is recent. Skipping download.",
                        "last_modified": modified_time.strftime("%Y-%m-%d %H:%M:%S")
                    })

        # If refresh is true or file is missing/outdated
        asyncio.run(edd.main())
        return jsonify({"status": "Data download completed successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)