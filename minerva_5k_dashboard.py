# cheatsheet: https://cheat-sheet.streamlit.app/
import streamlit as st
import plotly.express as px
import pandas as pd

# Data preparation
df = pd.DataFrame([
    {"Name": "Alex Smith", "Runs Completed": 5, "Best Time": "25:30", "Position": 1},
    {"Name": "Jamie Taylor", "Runs Completed": 4, "Best Time": "26:15", "Position": 2},
    {"Name": "Sam Rivera", "Runs Completed": 5, "Best Time": "27:00", "Position": 3},
    {"Name": "Jordan Lee", "Runs Completed": 3, "Best Time": "28:45", "Position": 4},
    {"Name": "Casey Jordan", "Runs Completed": 2, "Best Time": "30:00", "Position": 5},
])

# Dashboard layout
st.title('Minerva 5K Challenge Dashboard')

# Overview section
champion = df.loc[df['Position'].idxmin()]
st.markdown(f"### 🏆 Champion: {champion['Name']}")
st.markdown(f"**Best Time:** {champion['Best Time']} | **Runs Completed:** {champion['Runs Completed']}")

# Participant count
st.metric(label="Total Participants", value=len(df))

# Data visualization
st.subheader('📊 Performance Overview')
fig = px.bar(df, x='Name', y='Runs Completed', color='Position', 
             labels={'Position': 'Position Rank'}, 
             hover_data=['Best Time'], title="Runs Completed by Participants")
fig.update_layout(xaxis_title="Participant", yaxis_title="Runs Completed", 
                  coloraxis_showscale=False)
st.plotly_chart(fig, use_container_width=True)

# Search and detailed view
st.subheader('🔍 Find Participant Details')
participant_name = st.text_input('Enter a name to search:', '')
if participant_name:
    participant_details = df[df['Name'].str.contains(participant_name, case=False)]
    if not participant_details.empty:
        st.write(participant_details)
    else:
        st.warning('No participant found with this name.')

# Toggle for full participant table
if st.checkbox('Show All Participants'):
    st.subheader('👥 All Participants')
    st.dataframe(df.sort_values(by='Position'))

# Additional insights (Optional, can be added if needed)
with st.expander("See Additional Insights"):
    # Placeholder for any additional insights you might want to add
    st.text("Insights or extra data can go here.")

# Sidebar for quick filters (Optional)
st.sidebar.header('Quick Filters')
position_filter = st.sidebar.selectbox('Filter by Position:', ['All'] + list(df['Position'].unique()), index=0)

if position_filter != 'All':
    filtered_data = df[df['Position'] == position_filter]
    st.sidebar.dataframe(filtered_data[['Name', 'Best Time']])
else:
    st.sidebar.write("No filter applied.")
