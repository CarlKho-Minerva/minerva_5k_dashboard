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
st.write(winners)

import streamlit as st
import plotly.express as px
import pandas as pd

# Assuming df is already defined and sorted as in your setup

# Example conversion of "Best Time" for plotting (ensure this is done appropriately)
df['Best Time Seconds'] = df['Best Time'].dt.total_seconds()

# Plotting
fig_run_times = px.bar(df, x='Name', y='Best Time Seconds', color='Name', title="Run Times Leaderboard")
# Customize y-axis labels to display time in MM:SS format
fig_run_times.update_layout(yaxis_tickvals=[i * 60 for i in range(max(df['Best Time Seconds'])//60 + 1)], 
                            yaxis_ticktext=[f'{i:02d}:00' for i in range(max(df['Best Time Seconds'])//60 + 1)],
                            xaxis_title="Participant", 
                            yaxis_title="Best Time")

st.plotly_chart(fig_run_times, use_container_width=True)

# Tabs for different plots
tab1, tab2, tab3 = st.tabs(["Run Times Leaderboard", "Runs Completed", "Performance Overview"])

with tab1:
    st.subheader('🏃 Run Times Leaderboard')
    # Using bar chart to display run times
    fig_run_times = px.bar(df, x='Name', y='Best Time', color='Name', title="Run Times Leaderboard")
    fig_run_times.update_layout(xaxis_title="Participant", yaxis_title="Best Time", yaxis_tickformat='%H:%M:%S')
    st.plotly_chart(fig_run_times, use_container_width=True)

with tab2:
    st.subheader('🔢 Runs Completed')
    # Using bar chart to display runs completed
    fig_runs_completed = px.bar(df, x='Name', y='Runs Completed', color='Name', title="Runs Completed")
    fig_runs_completed.update_layout(xaxis_title="Participant", yaxis_title="Runs Completed")
    st.plotly_chart(fig_runs_completed, use_container_width=True)

with tab3:
    st.subheader('📊 Performance Overview')
    # Scatter plot (existing)
    df['Best Time Seconds'] = df['Best Time'].dt.total_seconds()  # Convert timedelta to seconds for plotting
    fig_scatter = px.scatter(df, x="Runs Completed", y="Best Time Seconds", size="Position", color="Name", hover_name="Name",
                             title="Performance Overview: Runs Completed vs. Best Time")
    fig_scatter.update_layout(xaxis_title="Runs Completed", yaxis_title="Best Time (Seconds)", yaxis_tickformat='%H:%M:%S')
    st.plotly_chart(fig_scatter, use_container_width=True)

# Reset 'Best Time' to original string format for display purposes
df['Best Time'] = df['Best Time'].dt.components.apply(lambda x: f"{x.minutes:02d}:{x.seconds:02d}", axis=1)

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
    filtered_participants = len(filtered_by_runs)
    st.metric(label="Filtered Participants", value=filtered_participants)



