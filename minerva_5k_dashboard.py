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
st.subheader('🏆 Winners & Performance Overview')
winners = df[df['Position'] == 1]
st.write(winners)

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

# Filters for dynamic exploration within Participant Details
position_to_highlight = st.selectbox('Highlight Position:', ['All'] + sorted(df['Position'].unique().tolist()))
if position_to_highlight != 'All':
    df_filtered = df[df['Position'] == position_to_highlight]
else:
    df_filtered = df
st.write(df_filtered)

# Display total and filtered participants
total_participants = len(df)
filtered_participants = len(df_filtered)
st.metric(label="Total Participants", value=total_participants)
st.metric(label="Filtered Participants", value=filtered_participants)

# Additional interactivity based on user input
num_runs_filter = st.slider('Filter by minimum runs completed:', 0, df['Runs Completed'].max(), 1)
filtered_by_runs = df[df['Runs Completed'] >= num_runs_filter]
if not filtered_by_runs.empty:
    st.write(filtered_by_runs)
