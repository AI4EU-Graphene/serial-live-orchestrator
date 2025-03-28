import asyncio
from EirGrid_Data_Download import async_eirgrid_downloader as edd
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-demand', methods=['GET'])
def get_demand():
    try:
        asyncio.run(edd.main())  # Call main with no arguments, as originally written
        return jsonify({"status": "Data download completed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
