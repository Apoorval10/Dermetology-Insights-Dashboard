import streamlit as st
from streamlit_option_menu import option_menu
import subprocess

st.set_page_config(layout="centered")

# Display a title above the centered image
st.markdown('<h1 style="color: black; text-align: center;">Dermatology Insights Dashboard</h1>', unsafe_allow_html=True)

# Set the background image
bg_img = '''
<style>
    [data-testid="stAppViewContainer"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-image: url('https://img.freepik.com/free-vector/tiny-dermatologists-examining-skin-patient-hospital_74855-17896.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        height: 100vh;
    }
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)

# Three buttons below the image
selected2 = option_menu(
    None, ["Overview", "Data Entry", "Visualizations"],  
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color":"black", "max-width": "1300px"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "center",
            "margin": "0px",
            "text-color":"white",
        },
        "nav-link-selected": {"background-color": "#3EB489"},
    },
)


# Run the appropriate Python file when a button is clicked
if selected2 == "Data Entry":
    subprocess.run(["streamlit", "run", "app.py"])

if selected2 == "Visualizations":
    subprocess.run(["streamlit", "run", "visual.py"])


# ...

if selected2 == "Overview":
    subprocess.run(["streamlit", "run", "overview.py"])

