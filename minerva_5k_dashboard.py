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

# Longest walk
longest_walk = df[df['walk_run'] == 'I walked'].sort_values(by='distance', ascending=False).head(1)

# Median runner/walker
median_time = df['total_seconds'].median()
df['time_difference'] = (df['total_seconds'] - median_time).abs()
median_runner = df.sort_values(by='time_difference').head(1)

# Prepare summary data for each plot
# Note: For more detailed plots, additional processing may be required

# Title for the dashboard
st.title('Minerva 5K Challenge Dashboard')

# Create tabs for new plots
tabs = st.tabs([
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

# Create content for each tab
for i, tab in enumerate(tabs):
    with tab:
        if i == 0:
            # Generate and display the "Participants by Gender" plot
            fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
            st.plotly_chart(fig, use_container_width=True)
        elif i == 1:
            # Generate and display the "Fastest Female Students" plot
            st.subheader("Fastest Female Students")
            if not fastest_female_students.empty:
                fig = px.bar(fastest_female_students, x='full_name', y='total_seconds', title="Fastest Female Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
        elif i == 2:
            # Generate and display the "Fastest Male Students" plot
            st.subheader("Fastest Male Students")
            if not fastest_male_students.empty:
                fig = px.bar(fastest_male_students, x='full_name', y='total_seconds', title="Fastest Male Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
        elif i == 3:
            # Generate and display the "Fastest Non-binary Students" plot
            st.subheader("Fastest Non-binary Students")
            if not fastest_non_binary_students.empty:
                fig = px.bar(fastest_non_binary_students, x='full_name', y='total_seconds', title="Fastest Non-binary Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
        elif i == 4:
            # Generate and display the "Fastest Faculty/Staff" plot
            st.subheader("Fastest Faculty/Staff")
            if not fastest_faculty_staff.empty:
                fig = px.bar(fastest_faculty_staff, x='full_name', y='total_seconds', title="Fastest Faculty/Staff")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
        elif i == 5:
            # Generate and display the "Runners/Walkers with at Least 15 5Ks" plot
            st.subheader("Runners/Walkers with at Least 15 5Ks")
            if not runners_with_at_least_15_5ks.empty:
                # For example, you might want to display a histogram of their running times or a bar chart of their distances
                pass
            else:
                st.write("No data available.")
        elif i == 6:
            # Generate and display the "Most Improved Running Time" plot
            st.subheader("Most Improved Running Time")
            st.write("This feature is not yet implemented.")
        elif i == 7:
            # Generate and display the "Longest Walk" plot
            st.subheader("Longest Walk")
            if not longest_walk.empty:
                fig = px.bar(longest_walk, x='full_name', y='distance', title="Longest Walk")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
        elif i == 8:
            # Generate and display the "Median Runner/Walker" plot
            st.subheader("Median Runner/Walker")
            if not median_runner.empty:
                fig = px.bar(median_runner, x='full_name', y='total_seconds', title="Median Runner/Walker")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available.")
