import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import altair as alt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.cm as cm
import subprocess

#mysql
import mysql.connector
conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dermatology insights dashboard"
            )
cursor = conn.cursor()

bg_img = '''
<style>
    [data-testid="stAppViewContainer"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-image: url('https://img.freepik.com/free-vector/turquoise-cloud-background_91008-163.jpg?');
        background-size: cover;
        background-repeat: no-repeat;
        height: 100vh;
    }
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)



# Apply custom CSS to style the title
title_style = (
    "color: black; "
    "text-align: center; "
    "font-size: 36px; "
    "font-weight: bold; "
    "padding-top: 20px;"  # Adjust padding or margins as needed
)

st.markdown(f'<h1 style="{title_style}">Dermatology Insights Dashboard</h1>', unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Overview","Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

#---------------------------------------------------OVERVIEW------------------------------------

if selected=='Overview':
    metadata = pd.read_csv("HAM10000_metadata.csv")
    metadata = metadata.replace({
        'nv': 'Melanocytic nevi',
        'mel': 'Melanoma',
        'bkl': 'Benign keratosis-like lesions ',
        'bcc': 'Basal cell carcinoma',
        'akiec': 'Actinic keratoses',
        'vasc': 'Vascular lesions',
        'df': 'Dermatofibroma'
    })

    # Display Header
    
    st.markdown('<h1 style="color: black;">Overview</h1>', unsafe_allow_html=True)

    # Assuming you have loaded your metadata DataFrame
    metadata = pd.read_csv("HAM10000_metadata.csv")

    # Define the filtering options using Streamlit components
    age_input = st.selectbox("Age:", ['All', '< 40', '< 60', '< 80'])
    genre_input = st.selectbox("Sex:", ['All', 'Male', 'Female'])
    local_input = st.selectbox("Localization:", ['All'] + list(metadata['localization'].unique()))
    patho_input = st.selectbox("Pathology:", ['All'] + list(metadata['dx'].unique()))

    # Filter the DataFrame based on user inputs
    filtered_data = metadata.copy()  # Start with the original data

    if age_input != 'All':
        filtered_data = filtered_data[filtered_data['age'] < int(age_input.lstrip('< '))]

    if genre_input != 'All':
        filtered_data = filtered_data[filtered_data['sex'] == genre_input.lower()]

    if local_input != 'All':
        filtered_data = filtered_data[filtered_data['localization'] == local_input]

    if patho_input != 'All':
        filtered_data = filtered_data[filtered_data['dx'] == patho_input]

    # Display the filtered data as a table using Streamlit
    st.write(filtered_data)


    # Gender distribution pie chart
    fig_pie = px.pie(filtered_data, names='sex')
    st.plotly_chart(fig_pie)

    # Age distribution histogram
    fig_age = px.histogram(filtered_data, x="age")
    st.plotly_chart(fig_age)

    # Localization distribution bar plot
    fig_localization = go.Figure(data=go.Bar(x=filtered_data['localization'].value_counts(), y=filtered_data['localization'].unique(), orientation='h'))
    st.plotly_chart(fig_localization)

    # Pathology distribution bar plot
    fig_patho = go.Figure(data=[
        go.Bar(name='Male', y=filtered_data['dx'][filtered_data['sex'] == 'male'].value_counts(), x=filtered_data['dx'].unique()),
        go.Bar(name='Female', y=filtered_data['dx'][filtered_data['sex'] == 'female'].value_counts(), x=filtered_data['dx'].unique())  
    ])
    st.plotly_chart(fig_patho)


#--------------------------------------Data Entry------------------------------------------------

if selected=='Data Entry':
    def get_all_periods():
        items = db.fetch_all_periods()
        periods = [item["key"] for item in items]
        return periods

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
        "Chattisgarh",
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

#---------------------------------------------------Visualization-------------------------------------------
if selected == "Data Visualization":
    subprocess.run(["streamlit", "run", "visual.py"])