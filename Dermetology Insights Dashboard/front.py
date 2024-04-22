import streamlit as st
import subprocess


st.set_page_config(layout="wide")
st.markdown(f'<h1>Welcome to Dermatology Insights Dashboard</h1>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Add content to cell (1,1)
with col1:
    img = '''
    <style>
        img {
            height: 80vh;
            width: 90vh;
        }
    </style>
    <img src='https://img.freepik.com/free-vector/site-stats-concept-illustration_114360-1434.jpg?w=740&t=st=1703015292~exp=1703015892~hmac=2bf04022fd834662d197a2eb4c9b5c3eac6d8fe62ba50480fbc6ad4876323123'>
    '''
    st.markdown(img, unsafe_allow_html=True)
    
# Add content to cell (1,2)
with col2:
    st.header("About")
    st.write("Dermatology Insights Dashboard offers comprehensive visualizations and analytics, aiding in the understanding of dermatological trends. With interactive charts and filtering options, it provides in-depth insights into patient demographics, diseases, and regional occurrences, empowering informed decision-making in dermatology.")
    selected5 = st.button('Explore')

    # Check if the button is clicked
    if selected5:
        subprocess.run(["streamlit", "run", "test.py"])


