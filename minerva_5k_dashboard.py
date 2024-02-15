import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQZwoA2WaL9ovbe41GtWwkazrgDdwz6kPBxPPqn__OEfCZEWzngqGKA0yKdwFMn9_g7yrgJWe-jjA8F/pub?output=csv')

# Renaming columns to make them easier to work with
df.columns = [
    "timestamp", "email", "full_name", "gender", "status", "walk_run", "time", "distance", "screenshot", "photos", "anything_else"
]

# Convert "time" from string to timedelta and calculate total seconds
df['time_td'] = pd.to_timedelta(df['time'])
df['total_seconds'] = df['time_td'].dt.total_seconds()

# Clean 'distance' to ensure it's numeric
df['distance'] = pd.to_numeric(df['distance'], errors='coerce')

# Unique Participants
unique_participants = df['email'].nunique()

# Participants by Gender
participants_by_gender = df.groupby('gender').size().reset_index(name='count')

# Fastest Female Students
fastest_female_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Female') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

# Fastest Male Students
fastest_male_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Male') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

# Fastest Non-binary Students
fastest_non_binary_students = df[(df['walk_run'] == 'I ran') & (df['gender'] == 'Non-binary') & (df['status'].isin(['Student', 'Alumni']))].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

# Fastest Faculty/Staff
fastest_faculty_staff = df[(df['walk_run'] == 'I ran') & (df['status'] == 'Staff/Faculty')].sort_values(by='total_seconds').drop_duplicates(subset=['email'], keep='first')

# Runners/Walkers with at Least 15 5Ks
runners_with_at_least_15_5ks = df.groupby('email').filter(lambda x: len(x) >= 15)

# Most Improved Running Time (%)
improvement_df = df[df['walk_run'] == 'I ran'].groupby('email').agg(max_pace=('total_seconds', 'max'), min_pace=('total_seconds', 'min'))
improvement_df['improvement'] = improvement_df['max_pace'] - improvement_df['min_pace']
improvement_df = improvement_df.sort_values(by='improvement', ascending=False)

# Longest Walk
longest_walk = df[df['walk_run'] == 'I walked'].sort_values(by='distance', ascending=False).head(1)

# Median Runner/Walker
median_time = df['total_seconds'].median()
df['median_diff'] = (df['total_seconds'] - median_time).abs()
median_runner = df.sort_values(by='median_diff').head(1)


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
            # "Participants by Gender" plot
            fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
            st.plotly_chart(fig, use_container_width=True)

        elif i == 1:
            # "Fastest Female Students" plot
            st.subheader("Fastest Female Students")
            if not fastest_female_students.empty:
                fig = px.bar(fastest_female_students, x='full_name', y='total_seconds', title="Fastest Female Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest female students.")

        elif i == 2:
            # "Fastest Male Students" plot
            st.subheader("Fastest Male Students")
            if not fastest_male_students.empty:
                fig = px.bar(fastest_male_students, x='full_name', y='total_seconds', title="Fastest Male Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest male students.")

        elif i == 3:
            # "Fastest Non-binary Students" plot
            st.subheader("Fastest Non-binary Students")
            if not fastest_non_binary_students.empty:
                fig = px.bar(fastest_non_binary_students, x='full_name', y='total_seconds', title="Fastest Non-binary Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest non-binary students.")

        elif i == 4:
            # "Fastest Faculty/Staff" plot
            st.subheader("Fastest Faculty/Staff")
            if not fastest_faculty_staff.empty:
                fig = px.bar(fastest_faculty_staff, x='full_name', y='total_seconds', title="Fastest Faculty/Staff")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest faculty/staff.")

        elif i == 5:
            # "Runners/Walkers with at Least 15 5Ks" plot
            st.subheader("Runners/Walkers with at Least 15 5Ks")
            if not runners_with_at_least_15_5ks.empty:
                # Assuming you have a column 'total_5ks' showing the count for each user
                fig = px.bar(runners_with_at_least_15_5ks, x='email', y='n', title="Runners/Walkers with at Least 15 5Ks")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No runners/walkers with at least 15 5Ks.")

        elif i == 6:
            # "Most Improved Running Time" plot
            st.subheader("Most Improved Running Time")
            if not improvement_df.empty:
                fig_improvement = px.bar(improvement_df.reset_index(), x='email', y='improvement', title="Most Improved Running Time")
                st.plotly_chart(fig_improvement, use_container_width=True)
            else:
                st.write("No data available for improvement.")

        elif i == 7:
            # "Longest Walk" plot
            st.subheader("Longest Walk")
            if not longest_walk.empty:
                fig = px.bar(longest_walk, x='full_name', y='distance', title="Longest Walk")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for the longest walk.")

        elif i == 8:
            # "Median Runner/Walker" plot
            st.subheader("Median Runner/Walker")
            if not median_runner.empty:
                fig = px.bar(median_runner, x='full_name', y='total_seconds', title="Median Runner/Walker")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No median runner/walker data available.")
