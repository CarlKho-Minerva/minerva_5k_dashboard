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

st.title('Minerva 5K Challenge Dashboard')

# Champion section
champion = df[df['Position'] == 1]
st.subheader('🏆 Champion')
st.write(champion)

# Data Visualization
st.subheader('📊 Data Visualization')
fig = px.scatter(df, x="Runs Completed", y="Best Time", size="Position", color="Name", hover_name="Name",
                 title="Performance Overview: Runs Completed vs. Best Time")
st.plotly_chart(fig, use_container_width=True)

# Interactive Search Bar
st.subheader('🔍 Search Participants')
search_query = st.text_input('Enter a name to search:')
if search_query:
    # Filter participants based on search
    filtered_participants = df[df['Name'].str.contains(search_query, case=False)].sort_values(by="Position")
    if not filtered_participants.empty:
        for _, row in filtered_participants.iterrows():
            st.write(f"{row['Name']} - Position: {row['Position']}")
    else:
        st.warning('No participant found with this name.')

# Toggleable Table of All Participants
if st.checkbox('Show All Participants'):
    st.subheader('👥 All Participants')
    st.write(df.sort_values(by="Position"))

# Sidebar (optional additions)
st.sidebar.header('Dashboard Controls')
# Example: sidebar metric display
st.sidebar.metric(label="Total Participants", value=len(df))
