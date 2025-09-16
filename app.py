# app.py
from flask import Flask, request, jsonify
import pandas as pd
from model import find_best_donors 

app = Flask(__name__)
try:
    donors_df = pd.read_excel('DONOR_DATA.xlsx')
    print("Donor data loaded successfully.")
except FileNotFoundError:
    print("Error: DONOR_DATA.xlsx not found! Make sure it's in the same folder.")
    donors_df = pd.DataFrame()

@app.route('/get_donors', methods=['POST'])
def get_donors_api():
    if donors_df.empty:
        return jsonify({"error": "Donor data not loaded."}), 500

    patient_request = request.json 
    

    request_data = {
        "blood_group": patient_request.get('blood_group'),
        "location": (patient_request.get('latitude'), patient_request.get('longitude'))
    }
    
    best_donors = find_best_donors(request_data, donors_df)
    
    return jsonify(best_donors)

if __name__ == '__main__':
    app.run(debug=True, port=5001)