import streamlit as st

# Sample data for the Minerva 5K challenge
records = [
    {"Name": "Alex Smith", "Runs Completed": 5, "Best Time": "25:30", "Position": 1},
    {"Name": "Jamie Taylor", "Runs Completed": 4, "Best Time": "26:15", "Position": 2},
    {"Name": "Sam Rivera", "Runs Completed": 5, "Best Time": "27:00", "Position": 3},
    {"Name": "Jordan Lee", "Runs Completed": 3, "Best Time": "28:45", "Position": 4},
    {"Name": "Casey Jordan", "Runs Completed": 2, "Best Time": "30:00", "Position": 5},
]

# Streamlit app
st.title('Minerva 5K Challenge Dashboard')

# Display winners
st.subheader('Winners')
for record in records:
    if record["Position"] == 1:
        st.write(f"🥇 {record['Name']} - Best Time: {record['Best Time']}")

# Display number of runs completed by each participant
st.subheader('Number of Runs Completed')
for record in records:
    st.write(f"{record['Name']}: {record['Runs Completed']} runs")

# Optionally, display the best time for each participant
st.subheader('Best Times')
for record in records:
    st.write(f"{record['Name']}: {record['Best Time']}")
