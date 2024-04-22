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
def connect_to_database():
    # Replace with your database details
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dermatology insights dashboard"
    )
    return conn


bg_img = '''
<style>
        [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/free-vector/turquoise-cloud-background_91008-163.jpg?');
        background-size: cover;
        background-repeat: no-repeat;
        }
</style>
'''
st.markdown(bg_img, unsafe_allow_html=True)
st.title("Data Visualizations")

# --- Data Visualization ---


try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dermatology insights dashboard"
    )
    
    query = "SELECT * FROM patient_info"  
    metadata = pd.read_sql(query, conn)
    
    sidebar_bg_color = '#AFF0F0'
    sidebar_css = f"""
        .css-1a4cflr {{
            background-color: {sidebar_bg_color} !important;
        }}
    """

    st.markdown(f'<style>{sidebar_css}</style>', unsafe_allow_html=True)
    st.sidebar.header("Filter Here:")

    # Sidebar filters
    age_options = ['All', '< 40', '< 60', '< 80']
    genre_options = ['All', 'Male', 'Female']
    localization_options = ['All'] + metadata['Localization'].unique().tolist()
    pathology_options = ['All'] + metadata['Pathology'].unique().tolist()
    state_options = ['All'] + metadata['State'].unique().tolist()

    age_filter = st.sidebar.selectbox('Age:', age_options, index=0)
    genre_filter = st.sidebar.selectbox('Gender:', genre_options, index=0)
    localization_filter = st.sidebar.selectbox('Localization:', localization_options, index=0)
    pathology_filter = st.sidebar.selectbox('Pathology:', pathology_options, index=0)
    state_filter = st.sidebar.selectbox('State:', state_options, index=0)

    # Filtering the dataframe based on user inputs
    filtered_data = metadata.copy()  # Start with the original data

    if age_filter != 'All':
        filtered_data = filtered_data[filtered_data['Age'] < int(age_filter.lstrip('< '))]

    if genre_filter != 'All':
        # Convert both the column values and the filter to lowercase for case-insensitive comparison
        filtered_data = filtered_data[filtered_data['Gender'].str.lower() == genre_filter.lower()]


    if localization_filter != 'All':
        filtered_data = filtered_data[filtered_data['Localization'] == localization_filter]

    if pathology_filter != 'All':
        filtered_data = filtered_data[filtered_data['Pathology'] == pathology_filter]
        
    if state_filter != 'All':
        filtered_data = filtered_data[filtered_data['State'] == state_filter]

    # Display the filtered data as a table using Streamlit
    st.write(filtered_data)
#-----------------------pie chart--------------------------------
    # Gender distribution pie chart
    fig_pie = px.pie(filtered_data, names='Gender',title='Gender Distribution')
    st.plotly_chart(fig_pie)
    
#------------ Age distribution histogram-------------------
    fig_age = px.histogram(filtered_data, x="Age",title='Age Count')
    st.plotly_chart(fig_age)
    
#-----------------------Bar plot-------------------------------
    # Bar plot for localization distribution using filtered data
    fig_localization = go.Figure(data=go.Bar(
        x=filtered_data['Localization'].value_counts(),
        y=filtered_data['Localization'].unique(),
        orientation='h')
    )

    fig_localization.update_layout(
        width=500,
        plot_bgcolor='#FFFFFF',
        xaxis_title="Disease Count",
        yaxis_title="Localization",
        title_text="Disease Localization"
    )

    # Display the bar plot using Streamlit
    st.plotly_chart(fig_localization)
    
    # Bar plot for pathology distribution using filtered data
    fig_patho = go.Figure(data=[
        go.Bar(
            name='male',
            y=filtered_data['Pathology'][filtered_data['Gender'] == 'male'].value_counts(),
            x=filtered_data['Pathology'].unique()
        ),
        go.Bar(
            name='female',
            y=filtered_data['Pathology'][filtered_data['Gender'] == 'female'].value_counts(),
            x=filtered_data['Pathology'].unique()
        )
    ])

    fig_patho.update_layout(plot_bgcolor='#FFFFFF')
    

#-----------------------------Bar plot2------------------------------
    def fetch_skin_disease_data(conn):
        cursor = conn.cursor()

        query = "SELECT State, Pathology, COUNT(*) as count FROM patient_info GROUP BY State, Pathology"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    def bar_plot(filtered_data):
        # Create DataFrame from filtered data
        df = pd.DataFrame(filtered_data, columns=['State', 'Pathology', 'Count'])

        # Convert 'Count' to integer
        df['Count'] = df['Count'].astype(int)

        # Animated bar plot using Plotly Express
        fig = px.bar(
            df,
            x='State',
            y='Count',
            color='Pathology',
            animation_frame='Pathology',
            title='Skin Disease Distribution Across States',
            labels={'Count': 'Number of Cases'}
        )

        # Set layout parameters for better visualization
        fig.update_layout(
            xaxis_title='State',
            yaxis_title='Number of Cases',
            showlegend=True,
            xaxis=dict(type='category'),
        )

        # Set y-axis tick format to display integers
        fig.update_yaxes(tickvals=list(range(int(df['Count'].max()) + 1)))

        # Display the animated bar plot using Streamlit
        st.plotly_chart(fig)

    # Replace metadata with filtered_data when calling fetch_skin_disease_data
    skin_disease_data = fetch_skin_disease_data(conn)

    # Call bar_plot with the filtered data
    bar_plot(skin_disease_data)
#-----------------------------------Pie2---------------------------------
    # Define the function to get pathology counts from filtered data
    def get_pathology_counts(filtered_data):
        pathology_counts = filtered_data['Pathology'].value_counts().reset_index()
        pathology_counts.columns = ['Pathology', 'count']
        return pathology_counts

    # Define the function to plot the pie chart using filtered data
    def plot_pie_chart(filtered_data):
        pathology_counts = get_pathology_counts(filtered_data)
        fig = px.pie(pathology_counts, values='count', names='Pathology', title='Distribution of Diseases')
        st.plotly_chart(fig)

    
    plot_pie_chart(filtered_data)




# ----------------------------scatter plot-----------------------------------------

    # def animated_scatter_plot(data):
    #     df = pd.DataFrame(data)

    #     fig = px.scatter(
    #         df,
    #         x='Age',
    #         y='State',
    #         color='Age',
    #         hover_name='Pathology',
    #         animation_frame='Age', 
    #         animation_group='State',
    #         title='Animated Scatter Plot: Age vs State',
    #         labels={'Age': 'Average Age', 'State': 'State'},
    #         size_max=55,
    #     )

    #     fig.update_layout(width=800, height=600)
    #     st.write(fig)

   
    # animated_scatter_plot(filtered_data)
#----------------------------stacked area chart-----------------------

    def stacked(filtered_data):
          
        fig = px.area(filtered_data, x='Age', color='Pathology', line_group='Gender', facet_col='Localization',
                    labels={'Age': 'Age'},
                    title='Age Distribution by Pathology, Gender, and Localization',
                    height=600, width=800)

        
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  
        fig.update_xaxes(matches='x')  

        
        st.plotly_chart(fig)
    stacked(filtered_data)
#---------------------------------------Bubble Plot------------------------
    def fetch_bubble(filtered_data):
        # Grouping by Age and Localization to get CaseCount
        grouped_data = filtered_data.groupby(['Age', 'Localization']).size().reset_index(name='CaseCount')
        return grouped_data.values.tolist()

    def plot_bubble(filtered_data):
        # Grouping by Age and Localization to get CaseCount
        grouped_data = filtered_data.groupby(['Age', 'Localization']).size().reset_index(name='CaseCount')

        ages = grouped_data['Age'].tolist()
        localizations = grouped_data['Localization'].tolist()
        case_counts = grouped_data['CaseCount'].tolist()

        # Increase bubble size by modifying the multiplier (here, multiplied by 10)
        bubble_sizes = [count * 50 for count in case_counts]

        fig = go.Figure(data=go.Scatter(
            x=ages,
            y=localizations,
            mode='markers',
            marker=dict(size=bubble_sizes,
                        color=ages,  # Coloring bubbles based on Age
                        colorscale='Viridis',  # Choose a colorscale
                        showscale=True
                        ),
            text=['Age: {}<br>Localization: {}'.format(a, loc) for a, loc in zip(ages, localizations)],  # Tooltip text
            hoverinfo='text'  # Show tooltip on hover
        ))

        # Add labels and title directly within the figure
        fig.update_layout(
            title='Bubble Plot: Age vs. Localization (Cases)',
            xaxis=dict(title='Age'),
            yaxis=dict(title='Localization')
        )

        st.plotly_chart(fig)


    def fetch_pathology_data(filtered_data):
        return filtered_data[['Age', 'Gender', 'Localization', 'Pathology']].values.tolist()
    bubble_data = fetch_bubble(filtered_data)
    plot_bubble(filtered_data)
    pathology_data = fetch_pathology_data(filtered_data)



#-----------------------------------------
    # def animated_radar_chart(filtered_data):
    #     # Assuming your 'filtered_data' is a Pandas DataFrame with columns: ['Age', 'Gender', 'Localization', 'Pathology']
    #     # Create a new column for unique frame identifiers
    #     filtered_data['Frame'] = filtered_data.groupby('Pathology').cumcount()

    #     # Define color scale for variables
    #     colorscale = ['red', 'blue', 'green']

    #     fig = go.Figure()

    #     for col, color in zip(['Age', 'Gender', 'Localization'], colorscale):
    #         fig.add_trace(go.Scatterpolar(
    #             r=filtered_data[col],
    #             theta=filtered_data['Frame'],
    #             mode='lines',
    #             name=col,
    #             line=dict(color=color),
    #             connectgaps=True
    #         ))

    #     fig.update_layout(
    #         polar=dict(
    #             radialaxis=dict(visible=True),
    #         ),
    #         showlegend=True,
    #         title='Comparison of Age, Gender, and Localization for Different Pathologies',
    #     )

    #     st.plotly_chart(fig)

    # # Now, call this function with your filtered data
    # animated_radar_chart(filtered_data)
#--------------------------------
    
   

    def main():
        

        # Establish a database connection
        db_connection = connect_to_database()

        # Close the database connection
        db_connection.close()


    




    selected = st.button('Back')

    # Check if the button is clicked
    if selected:
        subprocess.run(["streamlit", "run", "test.py"])

except mysql.connector.Error as e:
    st.error(f"Error: {e}")