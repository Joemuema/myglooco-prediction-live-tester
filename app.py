import streamlit as st
import requests
import json
from datetime import datetime

# Set up the page
st.set_page_config(page_title="MyGlooco API Tester", page_icon="🩸")
st.title("MyGlooco Real-Time API Tester 🩸")
st.write("Enter patient telemetry below to test the Hybrid Grey-Box Prediction Engine.")

# Securely load the token from Streamlit Secrets
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("API Token not found in secrets.")
    st.stop()

API_URL = "https://josephmuema-myglooco-api.hf.space/api/v1/predict"

# Build the Web Form
with st.form("telemetry_form"):
    col1, col2 = st.columns(2)
    with col1:
        user_id = st.text_input("User ID", value="github_tester_01")
        current_bg = st.number_input("Current BG (mg/dL)", value=120.0, step=1.0)
        weight = st.number_input("Body Weight (kg)", value=70.0, step=1.0)
    with col2:
        carbs = st.number_input("Carbs Eaten (g)", value=45.0, step=1.0)
        insulin = st.number_input("Insulin Dose (U)", value=4.0, step=0.1)
        
    submitted = st.form_submit_button("Run Prediction Engine")

# Execute the API Call
if submitted:
    payload = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "current_bg": current_bg,
        "carbs_g": carbs,
        "insulin_u": insulin,
        "body_weight_kg": weight,
        "meal_type": "None",
        "activity_type": "None",
        "bolus_type": "Standard",
        "activity_duration_min": 0.0,
        "activity_intensity": 0.0,
        "bwz_carb_input_g": carbs
    }
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    with st.spinner("Waking up API and running UKF assimilation..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                st.success("Prediction Generated Successfully!")
                st.json(response.json())
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")