import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSp4C-PJb0C-mJ4HstT1Svxc4aDQeEffTRzh[…]Evo-66ReR2M0VwRmSYM/pub?gid=1231808415&single=true&output=csv')

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

# Calculate improvement for each participant
df_sorted = df.sort_values(by='timestamp')
improvement_df = df_sorted.groupby('email').agg({'total_seconds': ['first', 'last']})
improvement_df.columns = ['time_before', 'time_after']
improvement_df['improvement_seconds'] = improvement_df['time_before'] - improvement_df['time_after']
improvement_df['improvement_percentage'] = (improvement_df['improvement_seconds'] / improvement_df['time_before']) * 100


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
                st.subheader("Other Female Participants")
                other_female = df[(df['gender'] == 'Female') & (df['status'].isin(['Student', 'Alumni'])) & (~df['full_name'].isin(fastest_female_students['full_name']))]
                if not other_female.empty:
                    fig_other_female = px.bar(other_female, x='full_name', y='total_seconds', title="Other Female Participants")
                    st.plotly_chart(fig_other_female, use_container_width=True)
                else:
                    st.write("No other female participants.")
            else:
                st.write("No data available.")
        elif i == 2:
            # Generate and display the "Fastest Male Students" plot
            st.subheader("Fastest Male Students")
            if not fastest_male_students.empty:
                fig = px.bar(fastest_male_students, x='full_name', y='total_seconds', title="Fastest Male Students")
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("Other Male Participants")
                other_male = df[(df['gender'] == 'Male') & (df['status'].isin(['Student', 'Alumni'])) & (~df['full_name'].isin(fastest_male_students['full_name']))]
                if not other_male.empty:
                    fig_other_male = px.bar(other_male, x='full_name', y='total_seconds', title="Other Male Participants")
                    st.plotly_chart(fig_other_male, use_container_width=True)
                else:
                    st.write("No other male participants.")
            else:
                st.write("No data available.")
        elif i == 3:
            # Generate and display the "Fastest Non-binary Students" plot
            st.subheader("Fastest Non-binary Students")
            if not fastest_non_binary_students.empty:
                fig = px.bar(fastest_non_binary_students, x='full_name', y='total_seconds', title="Fastest Non-binary Students")
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("Other Non-binary Participants")
                other_non_binary = df[(df['gender'] == 'Non-binary') & (df['status'].isin(['Student', 'Alumni'])) & (~df['full_name'].isin(fastest_non_binary_students['full_name']))]
                if not other_non_binary.empty:
                    fig_other_non_binary = px.bar(other_non_binary, x='full_name', y='total_seconds', title="Other Non-binary Participants")
                    st.plotly_chart(fig_other_non_binary, use_container_width=True)
                else:
                    st.write("No other non-binary participants.")
            else:
                st.write("No data available.")
        elif i == 4:
            # Generate and display the "Fastest Faculty/Staff" plot
            st.subheader("Fastest Faculty/Staff")
            if not fastest_faculty_staff.empty:
                fig = px.bar(fastest_faculty_staff, x='full_name', y='total_seconds', title="Fastest Faculty/Staff")
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("Other Faculty/Staff Participants")
                other_faculty_staff = df[(df['status'] == 'Staff/Faculty') & (~df['full_name'].isin(fastest_faculty_staff['full_name']))]
                if not other_faculty_staff.empty:
                    fig_other_faculty_staff = px.bar(other_faculty_staff, x='full_name', y='total_seconds', title="Other Faculty/Staff Participants")
                    st.plotly_chart(fig_other_faculty_staff, use_container_width=True)
                else:
                    st.write("No other faculty/staff participants.")
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
            if not improvement_df.empty:
                # Bar chart showing improvement for each participant
                fig_improvement = px.bar(improvement_df.reset_index(), x='email', y='improvement_seconds', 
                                          title="Most Improved Running Time")
                fig_improvement.update_xaxes(title='Participant Email')
                fig_improvement.update_yaxes(title='Improvement (Seconds)')
                st.plotly_chart(fig_improvement, use_container_width=True)

                # Data table showing improvement details
                st.subheader("Improvement Details")
                st.write(improvement_df.reset_index())

                # Bar chart showing improvement percentage for each participant
                fig_improvement_percentage = px.bar(improvement_df.reset_index(), x='email', y='improvement_percentage', 
                                                    title="Percentage Improvement in Running Time")
                fig_improvement_percentage.update_xaxes(title='Participant Email')
                fig_improvement_percentage.update_yaxes(title='Improvement Percentage')
                st.plotly_chart(fig_improvement_percentage, use_container_width=True)
            else:
                st.write("No data available.")
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
