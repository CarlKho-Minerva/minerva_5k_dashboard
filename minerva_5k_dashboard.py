import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv('Minerva.csv')

# Renaming columns to make them easier to work with
df.columns = [
    "timestamp", "email", "full_name", "gender", "status", "walk_run", "time", "distance", "screenshot", "photos", "anything_else"
]

# Convert "time" from string to timedelta and calculate total seconds
df['time_td'] = pd.to_timedelta(df['time'])
df['total_seconds'] = df['time_td'].dt.total_seconds()

# Clean 'distance' to ensure it's numeric
df['distance'] = pd.to_numeric(df['distance'], errors='coerce')

# Calculate statistics and prepare data for plots

# Participants count by gender
participants_by_gender = df.groupby('gender')['email'].nunique().reset_index(name='count')

# Fastest times by status and gender
fastest_female_students = df[(df['gender'] == 'Female') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').head(1)
fastest_male_students = df[(df['gender'] == 'Male') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').head(1)
fastest_non_binary_students = df[(df['gender'] == 'Non-binary') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').head(1)
fastest_faculty_staff = df[df['status'] == 'Staff/Faculty'].sort_values(by='total_seconds').head(1)

# Runners/walkers with at least 15 5Ks
runners_with_at_least_15_5ks = df.groupby('email').filter(lambda x: len(x) >= 15)

# Most improved running time
# This requires calculating the improvement for each participant, which is more complex and will be addressed separately

# Longest walk
longest_walk = df[df['walk_run'] == 'I walked'].sort_values(by='distance', ascending=False).head(1)

# Median runner/walker
median_time = df['total_seconds'].median()
df['time_difference'] = (df['total_seconds'] - median_time).abs()
median_runner = df.sort_values(by='time_difference').head(1)

# Prepare summary data for each plot
# Note: For more detailed plots, additional processing may be required

{
    "participants_by_gender": participants_by_gender,
    "fastest_female_students": fastest_female_students,
    "fastest_male_students": fastest_male_students,
    "fastest_non_binary_students": fastest_non_binary_students,
    "fastest_faculty_staff": fastest_faculty_staff,
    "runners_with_at_least_15_5ks": runners_with_at_least_15_5ks,
    "longest_walk": longest_walk,
    "median_runner": median_runner
}


st.title('Minerva 5K Challenge Dashboard')

# Create tabs for new plots
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Participants by Gender",
    "Fastest Female Students",
    "Fastest Male Students",
    "Fastest Non-binary Students",
    "Fastest Faculty/Staff",
    "Runners/Walkers with at Least 15 5Ks",
    "Most Improved Running Time",
    "Longest Walk",
    "Median Runner/Walker"
])

with tab1:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab6:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab7:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)

with tab8:
    # Generate and display the "Participants by Gender" plot
    fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
    st.plotly_chart(fig, use_container_width=True)


# Repeat the above process with appropriate modifications for each tab
# Use the prepared dataframes like `fastest_female_students`, `fastest_male_students`, etc., for plotting

# Note: For plots requiring more complex calculations (e.g., most improved running time),
# you may need to perform additional data processing.

# Ensure to adapt the dataset paths, column names, and specific processing as per your application's context.
