# app.py
from flask import Flask, request, jsonify
import pandas as pd
from model import find_best_donors
import os

app = Flask(__name__)

# Load donor data
try:
    donors_df = pd.read_csv('DONOR_DATA.csv')
    donors_df.rename(columns={
        "bloodGroup": "blood_group",
        "location.lat": "latitude",
        "location.lng": "longitude"
    }, inplace=True)
    print("Donor data loaded successfully.")
except FileNotFoundError:
    print("Error: DONOR_DATA1.csv not found! Make sure it's in the same folder.")
    donors_df = pd.DataFrame()

@app.route('/get_donors', methods=['POST'])
def get_donors_api():
    if donors_df.empty:
        return jsonify({"error": "Donor data not loaded."}), 500

    patient_request = request.json
    if not patient_request:
        return jsonify({"error": "Invalid JSON request body."}), 400

    request_data = {
        "blood_group": patient_request.get('blood_group'),
        "location": (patient_request.get('latitude'), patient_request.get('longitude'))
    }

    best_donors = find_best_donors(request_data, donors_df)
    return jsonify(best_donors)


from threading import Thread
from db_connection import start_mongo_listener

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    # Start MongoDB listener in background
    t = Thread(target=start_mongo_listener)
    t.daemon = True
    t.start()
    
    app.run(host="0.0.0.0", port=port)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))  # Use Railway provided port
#     app.run(host="0.0.0.0", port=port, debug=True)        # Bind to all interfaces
