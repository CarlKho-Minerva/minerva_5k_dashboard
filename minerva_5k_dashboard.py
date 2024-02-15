import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSp4C-PJb0C-mJ4HstT1Svxc4aDQeEffTRzht4OJNRTfrLnVppqA_K8jGrcvEvo-66ReR2M0VwRmSYM/pub?gid=1231808415&single=true&output=csv')

# Renaming columns to make them easier to work with
df.columns = [
    "timestamp", "email", "full_name", "gender", "status", "walk_run", "time", "distance", "screenshot", "photos", "anything_else"
]

# Anonymize full names and remove emails
df['full_name'] = df['full_name'].str.split().apply(lambda x: x[0] + ' ' + x[-1][0] if x else '')
df.drop(columns=['email'], inplace=True)

# Convert "time" from string to timedelta and calculate total seconds
df['time_td'] = pd.to_timedelta(df['time'])
df['total_seconds'] = df['time_td'].dt.total_seconds()

# Clean 'distance' to ensure it's numeric
df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
df['pace_per_mile'] = df['total_seconds'] / df['distance']

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

# Display the overall winner based on pace per mile
st.subheader('🏆 Overall Winner')
overall_winner = df.sort_values(by='pace_per_mile').head(1)
st.write(overall_winner[['full_name', 'gender', 'status', 'walk_run', 'time', 'distance', 'pace_per_mile']])



# First set of tabs for fastest participants
fastest_participants_tabs = st.tabs([
    "Fastest Female Students",
    "Fastest Male Students",
    "Fastest Non-binary Students",
    "Fastest Faculty/Staff",
])

# Content for the first set of tabs
for i, tab in enumerate(fastest_participants_tabs):
    with tab:
        if i == 0:
            # "Fastest Female Students" plot
            if not fastest_female_students.empty:
                fig = px.bar(fastest_female_students, x='full_name', y='total_seconds', title="Fastest Female Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest female students.")
        elif i == 1:
            # "Fastest Male Students" plot
            if not fastest_male_students.empty:
                fig = px.bar(fastest_male_students, x='full_name', y='total_seconds', title="Fastest Male Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest male students.")
        elif i == 2:
            # "Fastest Non-binary Students" plot
            if not fastest_non_binary_students.empty:
                fig = px.bar(fastest_non_binary_students, x='full_name', y='total_seconds', title="Fastest Non-binary Students")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest non-binary students.")
        elif i == 3:
            # "Fastest Faculty/Staff" plot
            if not fastest_faculty_staff.empty:
                fig = px.bar(fastest_faculty_staff, x='full_name', y='total_seconds', title="Fastest Faculty/Staff")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for fastest faculty/staff.")

# Second set of tabs for other metrics
other_metrics_tabs = st.tabs([
    "Participants by Gender",
    "Runners/Walkers with at Least 15 5Ks",
    "Most Improved Running Time",
    "Longest Walk",
    "Median Runner/Walker"
])

# Content for the second set of tabs
for i, tab in enumerate(other_metrics_tabs):
    with tab:
        if i == 0:
            # "Participants by Gender" plot
            fig = px.bar(participants_by_gender, x='gender', y='count', title="Participants by Gender")
            st.plotly_chart(fig, use_container_width=True)
        elif i == 1:
            # "Runners/Walkers with at Least 15 5Ks" plot
            if not runners_with_at_least_15_5ks.empty:
                fig = px.histogram(runners_with_at_least_15_5ks, x='email', title="Runners/Walkers with at Least 15 5Ks")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No runners/walkers with at least 15 5Ks.")
        elif i == 2:
            # "Most Improved Running Time" plot
            if not improvement_df.empty:
                fig_improvement = px.bar(improvement_df.reset_index(), x='email', y='improvement', title="Most Improved Running Time")
                st.plotly_chart(fig_improvement, use_container_width=True)
            else:
                st.write("No data available for improvement.")
        elif i == 3:
            # "Longest Walk" plot
            if not longest_walk.empty:
                fig = px.bar(longest_walk, x='full_name', y='distance', title="Longest Walk")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for the longest walk.")
        elif i == 4:
            # "Median Runner/Walker" plot
            if not median_runner.empty:
                fig = px.bar(median_runner, x='full_name', y='total_seconds', title="Median Runner/Walker")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No median runner/walker data available.")

# Participant Details with search functionality at the bottom
st.subheader('🔍 Search Participant Details')
participant_name = st.text_input('Enter a name to search:')
if participant_name:
    participant_details = df[df['full_name'].str.contains(participant_name, case=False, na=False)]
    if not participant_details.empty:
        st.write(participant_details[['full_name', 'gender', 'status', 'walk_run', 'time', 'distance', 'pace_per_mile']])
    else:
        st.warning('No participant found with this name.')

# Display table of all participants
st.subheader('👥 All Participants')
st.write(df[['full_name', 'gender', 'status', 'walk_run', 'time', 'distance', 'pace_per_mile']])
