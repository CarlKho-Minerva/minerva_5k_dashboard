import streamlit as st

# Sample data for the Minerva 5K challenge
records = [
    {"Name": "Alex Smith", "Runs Completed": 5, "Best Time": "25:30", "Position": 1},
    {"Name": "Jamie Taylor", "Runs Completed": 4, "Best Time": "26:15", "Position": 2},
    {"Name": "Sam Rivera", "Runs Completed": 5, "Best Time": "27:00", "Position": 3},
    {"Name": "Jordan Lee", "Runs Completed": 3, "Best Time": "28:45", "Position": 4},
    {"Name": "Casey Jordan", "Runs Completed": 2, "Best Time": "30:00", "Position": 5},
]

# Streamlit app layout
st.title('Minerva 5K Challenge Dashboard')

# Display winners with better formatting
st.subheader('🏆 Winners')
winner = next((record for record in records if record["Position"] == 1), None)
if winner:
    st.markdown(f"### 🥇 {winner['Name']} - Best Time: {winner['Best Time']}")

# Runs Completed - Visual Representation
st.subheader('🏃 Number of Runs Completed')
runs_data = {record['Name']: record['Runs Completed'] for record in records}
st.bar_chart(runs_data)

# Detailed View with Expander
with st.expander("See detailed view"):
    st.subheader('Participants Details')
    for record in records:
        st.markdown(f"""
        - **Name**: {record['Name']}
        - **Runs Completed**: {record['Runs Completed']}
        - **Best Time**: {record['Best Time']}
        - **Position**: {record['Position']}
        """)

# Optionally, add interactivity (Example: Filtering by number of runs)
min_runs = st.slider('Filter by minimum runs completed', 0, 5, 1)
filtered_records = [record for record in records if record['Runs Completed'] >= min_runs]
if filtered_records:
    st.subheader(f'Participants with at least {min_runs} runs')
    for record in filtered_records:
        st.text(f"{record['Name']}: {record['Runs Completed']} runs")
else:
    st.write("No participants with this minimum number of runs.")
