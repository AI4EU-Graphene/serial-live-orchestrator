from flask import Flask, jsonify
import pandas as pd
import os
import glob

app = Flask(__name__)

@app.route('/preprocess', methods=['GET'])
def preprocess():
    try:
        data_path = '/app/Downloaded_Data/'
        regions = ['ALL', 'ROI', 'NI']
        
        all_dfs = []

        for region in regions:
            region_files = glob.glob(os.path.join(data_path, region, "*.csv"))
            region_dfs = []

            for file in region_files:
                df = pd.read_csv(file, header=None, names=["Timestamp", "Type", "Region", "Value"])
                region_dfs.append(df)

            combined_region_df = pd.concat(region_dfs)
            all_dfs.append(combined_region_df)

        # Combine all regions into a single DataFrame
        combined_df = pd.concat(all_dfs)

        # Aggregate duplicates by taking mean value for same Timestamp-Type-Region
        aggregated_df = combined_df.groupby(['Timestamp', 'Region', 'Type']).agg({'Value': 'mean'}).reset_index()

        # Pivot the DataFrame to get types as separate columns, indexed by Timestamp and Region
        pivot_df = aggregated_df.pivot(index=['Timestamp', 'Region'], columns='Type', values='Value').reset_index()

        # Save the pivoted DataFrame
        output_file = '/app/Downloaded_Data/Combined_ALL_ROI_NI_pivoted_24.csv'
        pivot_df.to_csv(output_file, index=False)

        return jsonify({"status": f"Pivoted data saved successfully at {output_file}."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/', methods=['GET'])
def root():
    return "Data preprocessor is running.", 200
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
