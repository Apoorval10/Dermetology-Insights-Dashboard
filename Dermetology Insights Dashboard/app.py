import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import altair as alt


#mysql
import mysql.connector
conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dermatology insights dashboard"
            )
cursor = conn.cursor()



# -------------- SETTINGS --------------



page_title = "Dermatology Insights Dashboard"
page_icon = ":stethoscope:"  # emojis:
layout = "centered"






def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods

bg_img = '''
<style>
        [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/free-vector/clean-medical-background_53876-97927.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        }
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)

st.markdown('<h1 style="color: black;">Data Entry</h1>', unsafe_allow_html=True)


# Set up initial session state
session_state = st.session_state
if 'data_entry' not in session_state:
    session_state.data_entry = {
        'Age': None,
        'Gender': None
    }

# Age and gender options
black_text = """ 
    <style> 
        .black-text { 
            color: black !important; 
        } 
    </style> 
"""

# Apply the custom CSS styling
st.markdown(black_text, unsafe_allow_html=True)

patient_id = st.text_input("Patient ID:")
ages = st.text_input("Age:")
genders = ["--Select--","Male", "Female", "Other"]
localization = ["--Select--","scalp","ear","face","back","trunk","chest","upper extremity","abdomen","unknown","lower extremity","genital","neck","hand","foot","acral"]
pathology_list = ["--Select--",
    "Melanocytic nevi",
    "Melanoma",
    "Benign keratosis-like lesions",
    "Basal cell carcinoma",
    "Benign melanocytic lesions",
    "Vascular lesions",
    "Actinic keratoses",
    "Dermatofibroma"
]
states_in_india = ["--Select--",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]


# --------------------------------------



# Adding dropdowns for age and gender

selected_gender = st.selectbox("Gender:", genders)
selected_localization = st.selectbox("Localization:",localization)
selected_pathology_list=st.selectbox("Pathology:",pathology_list)
selected_states_in_india=st.selectbox("State:",states_in_india)

form = st.form(key='my_form')
submitted = form.form_submit_button("Save Data")
if submitted:
    try:
        
        
        # Prepare SQL query to insert data
        sql = "INSERT INTO patient_info(patient_id, age, gender, localization, pathology, state) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (patient_id, ages, selected_gender, selected_localization, selected_pathology_list, selected_states_in_india)

        # Execute the SQL query
        cursor.execute(sql, values)

        # Commit changes to the database
        conn.commit()
        st.success("Data saved!")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
        
        
        


    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            
            
