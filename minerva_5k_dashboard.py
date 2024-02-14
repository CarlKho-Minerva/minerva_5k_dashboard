# cheatsheet: https://cheat-sheet.streamlit.app/

import streamlit as st
import plotly.express as px # installed
import pandas as pd

# Convert the records to a DataFrame for better handling
df = pd.DataFrame([
    {"Name": "Alex Smith", "Runs Completed": 5, "Best Time": "25:30", "Position": 1},
    {"Name": "Jamie Taylor", "Runs Completed": 4, "Best Time": "26:15", "Position": 2},
    {"Name": "Sam Rivera", "Runs Completed": 5, "Best Time": "27:00", "Position": 3},
    {"Name": "Jordan Lee", "Runs Completed": 3, "Best Time": "28:45", "Position": 4},
    {"Name": "Casey Jordan", "Runs Completed": 2, "Best Time": "30:00", "Position": 5},
])

st.title('Minerva 5K Challenge Dashboard')

tab1, tab2, tab3 = st.tabs(["Winners", "Participant Details", "Data Visualization"])

with tab1:
    st.subheader('🏆 Winners')
    winners = df[df['Position'] == 1]
    st.write(winners)

with tab2:
    st.subheader('👥 Participant Details')
    participant_name = st.text_input('Enter a name to search:', '')
    if participant_name:
        participant_details = df[df['Name'].str.contains(participant_name, case=False)]
        if not participant_details.empty:
            st.write(participant_details)
        else:
            st.warning('No participant found with this name.')

with tab3:
    st.subheader('📊 Data Visualization')
    fig = px.scatter(df, x="Runs Completed", y="Best Time", size="Position", color="Name", hover_name="Name",
                     title="Performance Overview: Runs Completed vs. Best Time")
    st.plotly_chart(fig, use_container_width=True)

# Sidebar filters for dynamic exploration
st.sidebar.header('Filters')
position_to_highlight = st.sidebar.selectbox('Highlight Position:', ['All'] + sorted(df['Position'].unique().tolist()))

if position_to_highlight != 'All':
    df_filtered = df[df['Position'] == position_to_highlight]
else:
    df_filtered = df

st.sidebar.metric(label="Total Participants", value=len(df))
st.sidebar.metric(label="Filtered Participants", value=len(df_filtered))

# Use of progress and status
with st.expander("See calculation progress"):
    my_bar = st.progress(0)
    for percent_complete in range(100):
        my_bar.progress(percent_complete + 1)
    st.success('Data loaded successfully!')

# Additional interactivity based on user input
num_runs_filter = st.sidebar.slider('Filter by minimum runs completed:', 0, df['Runs Completed'].max(), 1)
filtered_by_runs = df[df['Runs Completed'] >= num_runs_filter]
st.sidebar.write(filtered_by_runs)
