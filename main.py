import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the Excel sheet into a pandas DataFrame
df = pd.read_excel('your_excel_file.xlsx')  # Replace with the actual path to your Excel file

@app.route('/get_iso_tank', methods=['POST'])
def get_iso_tank():
    # Get the input data from the form (either UN No. or Cargo Name)
    cargo = request.json.get('cargo')

    if not cargo:
        return jsonify({"error": "Cargo not provided"}), 400

    # Look for either the Cargo Name or UN No. match in the DataFrame
    result = df[(df['Cargo Name'].str.contains(cargo, case=False, na=False)) | (df['UN No.'] == cargo)]

    if not result.empty:
        # Extract the suitable ISO Tank from the DataFrame (Column Z is the 'UNTANKINS' column)
        iso_tank = result.iloc[0]['UNTANKINS']
        return jsonify({"iso_tank": iso_tank}), 200
    else:
        return jsonify({"error": "No suitable ISO Tank found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

