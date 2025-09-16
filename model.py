# model.py
import pandas as pd
from geopy.distance import geodesic
from datetime import datetime

BLOOD_COMPATIBILITY = {
    'A+' : ['O-', 'O+','A-','A+'],
    'A-' : ['O-','A-'],
    'B+' : ['O+','O-','B-','B+'],
    'B-' : ['O-','B-'],
    'AB+' : ['A+','A-','O-','O+','B+','B-','AB+','AB-'],
    'AB-' : ['O-','B-', 'A-', 'AB-'],
    'O+' : ['O-','O+'],
    'O-' : ['O-']
}


def safe_parse_date(date_value):
    if not date_value or str(date_value).lower() == "nan":
        # If no date → assume donor donated very long ago
        return datetime(2000, 1, 1)  
    try:
        return datetime.strptime(str(date_value), "%B %d %Y")  # expected format
    except ValueError:
        # If it’s in the wrong format, just return a very old date
        return datetime(2000, 1, 1)

def calculate_blood_score(patient_blood_group, donor_blood_group):
    if donor_blood_group in BLOOD_COMPATIBILITY.get(patient_blood_group,[]):
        return 1.0
    return 0.0

def calculate_distance_score(hospital_coords, donor_coords, max_radius_km = 10):
    distance = geodesic(hospital_coords, donor_coords).kilometers
    if distance > max_radius_km:
        return 0.0
    return (1.0 - (distance/max_radius_km)) # 0.8 if distance between both is 2kms 


MIN_DAYS_BETWEEN_DONATIONS = 90
#last_donation_date = datetime.strptime(donor['lastDonationDate'], "%B %d %Y")

def calculate_recency_score(last_donation_date):
    time_since_donation = datetime.now() - last_donation_date
    if time_since_donation.days < MIN_DAYS_BETWEEN_DONATIONS:
        return 0.0
    return 1.0  

def find_best_donors(patient_request, donors_df):
    WEIGHTS = {
        'distance': 0.7, 
        'recency': 0.3   
    }

    scores = []
    
    for index, donor in donors_df.iterrows():
        blood_score = calculate_blood_score(patient_request['blood_group'], donor['blood_group'])
        
        # If not compatible, skip this donor entirely
        if blood_score == 0:
            continue
            
        # 2. Distance Score
        hospital_coords = patient_request['location']
        donor_coords = (donor['latitude'], donor['longitude'])
        distance_score = calculate_distance_score(hospital_coords, donor_coords)

        # If outside radius, score is 0, so they will be ranked low
        if distance_score == 0:
            continue
        
        last_donation_date = safe_parse_date(donor['lastDonationDate'])
        recency_score = calculate_recency_score(last_donation_date)
        
        # If ineligible, skip
        if recency_score == 0:
            continue

        # 4. Final Weighted Score
        final_score = (distance_score * WEIGHTS['distance']) + (recency_score * WEIGHTS['recency'])
        
        scores.append({
            'donor_id': donor.name,
            'name': donor['name'],
            'blood_group': donor['blood_group'],
            'compatibility_score': round(final_score * 100, 2), # Present as a percentage
            'distance_km': round(geodesic(hospital_coords, donor_coords).kilometers, 2)
        })
        
    # Sort by score in descending order and return top 5
    ranked_donors = sorted(scores, key=lambda x: x['compatibility_score'], reverse=True)
    
    return ranked_donors[:5]