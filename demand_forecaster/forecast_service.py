from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def forecast():
    try:
        file_path = '/app/Downloaded_Data/ALL/ALL_demandactual_24_Eirgrid.csv'
        
        if not os.path.exists(file_path):
            return jsonify({"error": "Data file not found."}), 404

        # Load CSV
        df = pd.read_csv(file_path, header=None)

        # Preview and basic info
        preview = df.head(5).to_dict(orient='records')
        row_count = len(df)

        return jsonify({
            "status": "Data loaded",
            "preview": preview,
            "rows": row_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
