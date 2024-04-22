import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# LOADING AND PREPROCESS DATA 
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

bg_img = '''
<style>
        [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/premium-vector/abstract-technology-hexagons-background_41814-261.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        }
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)
st.title("SKIN DISEASE DASHBOARD")
st.markdown("This app is intended for visualizing health data from 10,000 patients suffering from skin diseases.")



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
