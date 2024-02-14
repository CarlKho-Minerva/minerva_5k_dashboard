# cheatsheet: https://cheat-sheet.streamlit.app/

import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame([
    {"Name": "Alex Smith", "Runs Completed": 5, "Best Time": "25:30", "Position": 1},
    {"Name": "Jamie Taylor", "Runs Completed": 4, "Best Time": "26:15", "Position": 2},
    {"Name": "Sam Rivera", "Runs Completed": 5, "Best Time": "27:00", "Position": 3},
    {"Name": "Jordan Lee", "Runs Completed": 3, "Best Time": "28:45", "Position": 4},
    {"Name": "Casey Jordan", "Runs Completed": 2, "Best Time": "30:00", "Position": 5},
])

# Dashboard Title
st.title('Minerva 5K Challenge Dashboard')

# Winners and Data Visualization
st.subheader('🏆 Winner')
winners = df[df['Position'] == 1]
st.header(winners)

fig = px.scatter(df, x="Runs Completed", y="Best Time", size="Position", color="Name", 
                 hover_name="Name", title="Runs Completed vs. Best Time")
st.plotly_chart(fig, use_container_width=True)

# Participant Details
st.subheader('👥 Participant Details')
participant_name = st.text_input('Enter a name to search:', '')
if participant_name:
    participant_details = df[df['Name'].str.contains(participant_name, case=False)]
    if not participant_details.empty:
        st.write(participant_details)
    else:
        st.warning('No participant found with this name.')

# Additional interactivity based on user input
num_runs_filter = st.slider('Filter by minimum runs completed:', 0, df['Runs Completed'].max(), 1)
filtered_by_runs = df[df['Runs Completed'] >= num_runs_filter]
if not filtered_by_runs.empty:
    st.write(filtered_by_runs)

# Display total and filtered participants in 2-column layout
col1, col2 = st.columns(2)
with col1:
    total_participants = len(df)
    st.metric(label="Total Participants", value=total_participants)
with col2:
    filtered_participants = len(df_filtered)
    st.metric(label="Filtered Participants", value=filtered_participants)



