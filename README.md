# Blood Donor Compatibility Model 🩸

This is the AI/ML component for the **Khoon Connect** hackathon project. It is a lightweight, heuristic-based ranking model that runs as a standalone Flask API. Its sole purpose is to receive a patient's blood request and instantly return a ranked list of the most suitable donors from a database.

---

## ⚙️ How It Works

Instead of a traditional trained model, this project uses a high-speed, rule-based AI ranking system to ensure real-time results. It calculates a **Compatibility Score** for every donor based on a weighted formula that prioritizes the most critical factors in an emergency.

The scoring logic is as follows:

1.  **Blood Type Compatibility (Pass/Fail):** The model first checks if the donor's blood type is compatible with the patient's. If not, the donor is immediately discarded.
2.  **Donation Recency (Pass/Fail):** It then checks if the donor has donated within the last 90 days. If so, they are considered ineligible and discarded.
3.  **Proximity Score (Weighted):** For all remaining donors, a distance score is calculated. This score is normalized, giving donors who are closer to the hospital a significantly higher score.
4.  **Final Ranking:** The model returns a sorted list of the top 5 donors with the highest final scores.

---

## 🛠️ Technology Stack

* **Language:** Python 3.9+
* **API Framework:** Flask
* **Data Handling:** Pandas
* **Geospatial Calculations:** Geopy
* **Excel File Reading:** openpyxl

---

## 🚀 Setup and Installation

### Prerequisites

* Python 3.9+ and `pip` installed.

### Steps

1.  **Clone the repository and navigate to the model directory:**
    ```bash
    git clone [https://github.com/your-username/khoon-connect.git](https://github.com/your-username/khoon-connect.git)
    cd khoon-connect/blood-compatibility-model
    ```

2.  **Install the required Python packages:**
    ```bash
    # First, create the requirements.txt file
    pip freeze > requirements.txt

    # Then, install from it
    pip install -r requirements.txt
    ```

3.  **Place the dataset:**
    Ensure your donor dataset, named **`DONOR_DATA.xlsx`**, is present in this directory.

4.  **Run the API server:**
    ```bash
    python app.py
    ```
    The server will start and listen for requests on `http://127.0.0.1:5001`.

---

## 🔌 API Documentation

The model exposes a single endpoint for finding donors.

### Endpoint: `POST /get_donors`

This endpoint receives patient details and returns a ranked list of the top 5 most suitable donors.

#### Request Body

The request must be a JSON object containing the patient's blood group and current location.

```json
{
  "blood_group": "A+",
  "latitude": 19.0760,
  "longitude": 72.8777
}
