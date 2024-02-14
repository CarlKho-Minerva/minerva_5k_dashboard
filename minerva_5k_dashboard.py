import streamlit as st
import plotly.express as px
import pandas as pd

# Load the data
df = pd.read_csv("/mnt/data/Minerva.csv")

# Clean and preprocess the data
# Assuming the time column is named 'time' and formatted like 'HH:MM:SS'
df['Total Seconds'] = pd.to_timedelta(df['time']).dt.total_seconds()

# Calculate the number of runs completed by each participant
df['Runs Completed'] = df.groupby('Email Address')['Email Address'].transform('count')

# Calculate the best time for each participant
df['Best Time'] = df.groupby('Email Address')['Total Seconds'].transform('min')

# Add a Position column based on the best time
df['Position'] = df.groupby('Email Address')['Total Seconds'].rank("dense", ascending=True)

# Now you can use this DataFrame (df) in your Streamlit app for visualization
st.title('Minerva 5K Challenge Dashboard')

# Winners and Data Visualization
st.subheader('🏆 Winners')
winners = df[df['Position'] == 1]
st.write(winners[['Email Address', 'Best Time', 'Runs Completed', 'Position']])

# Creating tabs for each plot
tab1, tab2, tab3 = st.tabs(["Performance Overview", "Run Times", "Runs Completed"])

with tab1:
    st.subheader("Performance Overview: Runs Completed vs. Best Time")
    fig1 = px.scatter(df, x="Runs Completed", y="Best Time", size="Position", color="Email Address", hover_name="Email Address")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Run Times Overview (Lower is Better)")
    fig2 = px.bar(df, x="Email Address", y="Total Seconds", color="Email Address")
    fig2.update_layout(xaxis_title="Participant Email", yaxis_title="Total Seconds (Best Recorded Times)")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Runs Completed Overview")
    fig3 = px.bar(df, x="Email Address", y="Runs Completed", color="Email Address")
    fig3.update_layout(xaxis_title="Participant Email", yaxis_title="Runs Completed")
    st.plotly_chart(fig3, use_container_width=True)

# Participant Details
st.subheader('👥 Participant Details')
participant_email = st.text_input('Enter an email to search:', '')
if participant_email:
    participant_details = df[df['Email Address'].str.contains(participant_email, case=False)]
    if not participant_details.empty:
        st.write(participant_details[['Email Address', 'Runs Completed', 'Best Time', 'Position']])
    else:
        st.warning('No participant found with this email.')

# Additional interactivity based on user input
num_runs_filter = st.slider('Filter by minimum runs completed:', 0, df['Runs Completed'].max(), 1)
filtered_by_runs = df[df['Runs Completed'] >= num_runs_filter]
if not filtered_by_runs.empty:
    st.write(filtered_by_runs[['Email Address', 'Runs Completed', 'Best Time', 'Position']])

# Display total and filtered participants in 2-column layout
col1, col2 = st.columns(2)
with col1:
    total_participants = df['Email Address'].nunique()
    st.metric(label="Total Participants", value=total_participants)
with col2:
    filtered_participants = filtered_by_runs['Email Address'].nunique()
    st.metric(label="Filtered Participants", value=filtered_participants)
